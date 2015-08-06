from flask import current_app
import Image
from os import mkdir, remove
from os.path import exists, join
from project.bl.utils import BaseBL
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
        category_dir = join(
            current_app.config['UPLOAD_FOLDER'],
            img_category.name
        )
        mkdir_ifn_exists(category_dir)

        thumbnail_dir = join(category_dir, 'thumb')
        fullsized_dir = join(category_dir, 'full')
        mkdir_ifn_exists(thumbnail_dir)
        mkdir_ifn_exists(fullsized_dir)

        uid = uuid4().hex
        ext = image.filename.rsplit('.', 1)[1]
        uid += '.' + ext
        image.save(join(fullsized_dir, uid))
        thumb = Image.open(join(fullsized_dir, uid))
        thumb.thumbnail((75, 75), Image.NEAREST)
        thumb.save(join(thumbnail_dir, uid))

        uploaded_image = self.model(
            uid=uid,
            img_category=img_category,
            title=kwargs.pop('title'),
            description=kwargs.pop('description'),
        )
        uploaded_image.bl.save()

    def delete(self):
        cat = self.model.img_category
        uid = self.model.uid
        category_dir = join(
            current_app._config['UPLOAD_DIR'],
            cat.name
        )
        thumbnail_dir = join(category_dir, 'thumb')
        fullsized_dir = join(category_dir, 'full')
        remove(join(thumbnail_dir, uid))
        remove(join(fullsized_dir, uid))
        super().delete()
