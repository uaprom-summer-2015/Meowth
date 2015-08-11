from abc import ABCMeta, abstractmethod
from uuid import uuid4
import os
import cloudinary

from cloudinary.utils import cloudinary_url
from flask import url_for, current_app
from werkzeug.utils import secure_filename

from project.tasks.uploads import celery_make_thumbnail


def generate_file_path(category, name, ext):
    return "{category}/full/{name}.{ext}".format(
        category=category,
        name=name,
        ext=ext
    )


class ImageHandler(metaclass=ABCMeta):
    @abstractmethod
    def get_full_image_url(self, path):
        pass

    @abstractmethod
    def upload(self, *, image, img_category, **kwargs):
        pass


class FlaskImageHandler(ImageHandler):
    def get_full_image_url(self, path):
        rel_path = url_for("get_file", path=path)
        return current_app.config["SERVER_NAME"] + rel_path

    def upload(self, *, image, img_category, **kwargs):
        def mkdir_ifn_exists(dirpath):
            if not os.path.exists(dirpath):
                os.mkdir(dirpath, mode=0o751)

        if image is None:
            return
        if 'title' not in kwargs:
            kwargs['title'] = secure_filename(image.filename)

        mkdir_ifn_exists(current_app.config['UPLOAD_FOLDER'])
        category_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            img_category.name,
        )
        mkdir_ifn_exists(category_dir)

        thumbnail_dir = os.path.join(category_dir, 'thumb')
        fullsized_dir = os.path.join(category_dir, 'full')
        mkdir_ifn_exists(thumbnail_dir)
        mkdir_ifn_exists(fullsized_dir)

        name = uuid4().hex
        ext = os.path.splitext(image.filename)[1][1:]
        filename = "{}.{}".format(name, ext)
        image.save(os.path.join(fullsized_dir, filename))

        celery_make_thumbnail.delay(
            path_to_original=os.path.join(fullsized_dir, filename),
            destination=os.path.join(thumbnail_dir, filename),
            size=(75, 75),
        )
        return name, ext


class CloudinaryImageHandler(ImageHandler):
    def get_full_image_url(self, path):
        return cloudinary_url(path)

    def upload(self, *, image, img_category, **kwargs):
        name = uuid4().hex
        ext = os.path.splitext(image.filename)[1][1:]
        filepath = generate_file_path(
            category=img_category,
            name=name,
            ext=ext
        )

        cloudinary.uploader.upload(
            image,
            public_id=filepath,
        )

        return name, ext


class SmartImageHandler:
    _handlers = {
        "flask": FlaskImageHandler,
        "cloudinary": CloudinaryImageHandler
    }
    _handler = None

    def __getattr__(self, name):
        if not self._handler:
            self._handler = self._handlers[current_app.config['IMAGE_SERVER']]()

        return getattr(self._handler, name)

