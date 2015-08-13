from flask import current_app
from os import remove
from os.path import join
from project.bl.utils import BaseBL
from project.extensions import imageHandler
from project.lib.media.media import generate_file_path


class UploadedImageBL(BaseBL):

    def get_full_url(self):
        return imageHandler.get_image_url(generate_file_path(
            self.model.type,
            self.model.name,
            self.model.ext
        ))

    def save_image(self, *, image, img_category, **kwargs):

        filename, ext = imageHandler.upload(
            image=image,
            img_category=img_category,
            **kwargs
        )

        uploaded_image = self.model(
            name=filename,
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
