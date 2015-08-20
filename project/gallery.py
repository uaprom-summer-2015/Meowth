from werkzeug.datastructures import FileStorage
from project.models import UploadedImage
from unittest.mock import patch
from project.tasks.uploads import celery_make_thumbnail as make_thumbnail


def load_images(count=100):
    for _ in range(count):
        with open('testdata/images/face-2.jpg', 'rb') as fp:
            file = FileStorage(fp)
            with patch(
                target='project.tasks.uploads.celery_make_thumbnail.delay',
                new=make_thumbnail,
            ):
                UploadedImage.bl.save_image(
                    image=file,
                    img_category=UploadedImage.IMG_CATEGORY.gallery,
                )
