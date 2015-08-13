from flask import current_app
from os import mkdir, remove
from os.path import exists, join, splitext
from project.bl.utils import BaseBL
from project.tasks.uploads import celery_make_thumbnail
from uuid import uuid4
from werkzeug import secure_filename


class UploadedImageBL(BaseBL):

    def save_image(self, *, image, img_category, **kwargs):

        def mkdir_ifn_exists(dirpath):
            if not exists(dirpath):
                mkdir(dirpath, mode=0o751)

        if image is None:
            return
        if 'title' not in kwargs:
            kwargs['title'] = secure_filename(image.filename)

        mkdir_ifn_exists(current_app.config['UPLOAD_FOLDER'])
        category_dir = join(
            current_app.config['UPLOAD_FOLDER'],
            img_category.name,
        )
        mkdir_ifn_exists(category_dir)

        thumbnail_dir = join(category_dir, 'thumb')
        fullsized_dir = join(category_dir, 'full')
        mkdir_ifn_exists(thumbnail_dir)
        mkdir_ifn_exists(fullsized_dir)

        uid = uuid4().hex
        ext = splitext(image.filename)[1][1:]
        name = "{}.{}".format(uid, ext)
        image.save(join(fullsized_dir, name))

        celery_make_thumbnail.delay(
            path_to_original=join(fullsized_dir, name),
            destination=join(thumbnail_dir, name),
            size=(75, 75),
        )

        uploaded_image = self.model(
            name=uid,
            ext=ext,
            img_category=img_category,
            title=kwargs.pop('title'),
            description=kwargs.pop('description'),
        )
        uploaded_image.bl.save()

    def delete(self):
        instance = self.model
        uid = instance.name.hex
        name = "{}.{}".format(uid, instance.ext)
        category_dir = join(
            current_app.config['UPLOAD_FOLDER'],
            instance.img_category.name
        )
        thumbnail_dir = join(category_dir, 'thumb')
        fullsized_dir = join(category_dir, 'full')
        remove(join(thumbnail_dir, name))
        remove(join(fullsized_dir, name))
        super().delete()
