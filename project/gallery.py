from project import app
from werkzeug.datastructures import FileStorage
from project.models import UploadedImage

with app.app_context():
    for _ in range(100):
        with open('testdata/face-2.jpg', 'rb') as fp:
            file = FileStorage(fp)
            UploadedImage.bl.save_image(
                image=file,
                img_category=UploadedImage.IMG_CATEGORY.gallery,
            )
