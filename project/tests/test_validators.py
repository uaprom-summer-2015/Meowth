from os.path import join
from project import app
from project.lib.media.validators import AllowedMime
from project.tests.utils import ProjectTestCase


class TessValidators(ProjectTestCase):

    def setUp(self):
        self.mimes = app.config['IMG_MIMES']
        self.datadir = join(self.app.config['BASEDIR'], 'project', 'tests',
                            'testdata', 'validators')

    def test_positive(self):
        with open(join(self.datadir, 'validimage.jpg')) as image:
            buf = image.buffer.read()
        self.assertTrue(AllowedMime.validate(
            buf=buf,
            mimes=self.mimes,
        ))

    def test_negative(self):
        with open(join(self.datadir, 'textfile.jpg')) as image:
            buf = image.buffer.read()
        self.assertFalse(AllowedMime.validate(
            buf=buf,
            mimes=self.mimes,
        ))
