from werkzeug.datastructures import FileStorage
from project.models import UploadedImage


def load_images(count=100):
    for _ in range(count):
        with open('testdata/face-2.jpg', 'rb') as fp:
            file = FileStorage(fp)
            UploadedImage.bl.save_image(
                image=file,
                img_category=UploadedImage.IMG_CATEGORY.gallery,
            )
