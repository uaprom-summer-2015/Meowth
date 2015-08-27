from flask import current_app, url_for
from pathlib import Path
from project.bl.utils import BaseBL
from project.tasks.uploads import celery_make_thumbnail
from uuid import uuid4
from werkzeug import secure_filename


class UploadedImageBL(BaseBL):

    def save_image_file(self, *, image, img_category, do_sync=False, **kwargs):
        def mkdir_ifn_exists(dirpath):
            if not dirpath.exists():
                dirpath.mkdir(mode=0o751, parents=True)

        make_thumbnail = (
            celery_make_thumbnail if do_sync else celery_make_thumbnail.delay
        )

        category_dir = Path(
            current_app.config['UPLOAD_FOLDER'],
            img_category.name,
        )

        thumbnail_dir = category_dir / 'thumb'
        fullsized_dir = category_dir / 'full'
        mkdir_ifn_exists(thumbnail_dir)
        mkdir_ifn_exists(fullsized_dir)

        uid = uuid4().hex
        ext = Path(image.filename).suffix[1:]
        name = "{}.{}".format(uid, ext)
        image.save(str(fullsized_dir / name))

        make_thumbnail(
            path_to_original=str(fullsized_dir / name),
            destination=str(thumbnail_dir / name),
            size=(200, 200),
        )
        return (uid, ext, img_category)

    def save_image(self, *, image, img_category, do_sync=False, **kwargs):
        if image is None:
            return
        if 'title' not in kwargs:
            kwargs['title'] = secure_filename(image.filename)

        uid, ext, category = self.save_image_file(
            image=image,
            img_category=img_category,
            do_sync=do_sync,
        )

        uploaded_image = self.create({
            'name': uid,
            'ext': ext,
            'img_category': img_category,
            'title': kwargs.get('title', None),
            'description': kwargs.get('description', None),
        })
        return uploaded_image

    def delete(self):
        instance = self.model
        uid = instance.name.hex
        name = "{}.{}".format(uid, instance.ext)
        category_dir = Path(
            current_app.config['UPLOAD_FOLDER'],
            instance.img_category.name
        )
        thumbnail = category_dir / 'thumb' / name
        fullsized = category_dir / 'full' / name
        if thumbnail.exists():
            thumbnail.unlink()
        if fullsized.exists():
            fullsized.unlink()
        super().delete()

    def get_url(self, is_thumbnail=False):
        model = self.model
        img_type = 'thumb' if is_thumbnail else 'full'
        filepath = '{}/{}/{}.{}'.format(
            model.img_category.name,
            img_type,
            model.name.hex,
            model.ext,
        )
        return url_for('get_file', path=filepath, _external=True)
