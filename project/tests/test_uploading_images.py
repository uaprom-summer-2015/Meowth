import shutil
import pathlib
from project.models import UploadedImage
from project.tasks.uploads import celery_make_thumbnail as make_thumbnail
from unittest.mock import patch
from werkzeug.datastructures import FileStorage, Headers
from project.tests.utils import ProjectTestCase
import tempfile


class TestUploadImage(ProjectTestCase):

    def setUp(self):
        self.app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        self.upload_folder = pathlib.Path(self.app.config['UPLOAD_FOLDER'])
        path = pathlib.Path(self.app.config['BASEDIR'])
        path = (
            path / 'project' /
            'tests' / 'testdata' /
            'images' / 'testimage1.jpg'
        )
        imagefile = FileStorage(
            stream=open(str(path), 'br'),
            filename=str(path),
            headers=Headers([('Content-Type', 'image/jpeg')]),
        )
        with patch(
            target='project.tasks.uploads.celery_make_thumbnail.delay',
            new=make_thumbnail,
        ):
            UploadedImage.bl.save_image(
                image=imagefile,
                img_category=UploadedImage.IMG_CATEGORY.other,
                title='testing image',
                description='testing image',
            )
        imagefile.close()

    def tearDown(self):
        super(TestUploadImage, self).tearDown()
        path = self.upload_folder
        if path.exists():
            shutil.rmtree(str(path))

    def test_save_image(self):
        img = (
            UploadedImage.query
            .filter(UploadedImage.title == 'testing image')
            .filter(UploadedImage.description == 'testing image')
            .first()
        )
        self.assertIsNotNone(img)
        pathes = [
            (
                self.upload_folder / img.img_category.name / folder
                / ('%s.%s' % (img.name.hex, img.ext))
            ) for folder in {'full', 'thumb'}
        ]
        for path in pathes:
            self.assertTrue(path.exists())

    def test_delete_image(self):
        img = (
            UploadedImage.query
            .filter(UploadedImage.title == 'testing image')
            .filter(UploadedImage.description == 'testing image')
            .first()
        )
        self.assertIsNotNone(img)
        pathes = [
            (
                self.upload_folder / img.img_category.name / folder
                / ('%s.%s' % (img.name.hex, img.ext))
            ) for folder in {'full', 'thumb'}
        ]
        img.bl.delete()
        for path in pathes:
            self.assertFalse(path.exists())
