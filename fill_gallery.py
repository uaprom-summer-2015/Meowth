from project import app
from project.models import UploadedImage
from werkzeug.datastructures import FileStorage

with app.app_context():
    for _ in range(100):
        with open('face.png', 'rb') as fp:
            file = FileStorage(fp)
            UploadedImage.bl.save_image(
                image=file,
                img_category = UploadedImage.IMG_CATEGORY.gallery
            )
