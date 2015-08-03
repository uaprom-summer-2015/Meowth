from project.lib.media.validators import allowed_file
from project.tests.utils import ProjectTestCase


class TessValidators(ProjectTestCase):

    def test_allowed_files(self):
        self.assertTrue(allowed_file('spam.doc'))
        self.assertFalse(allowed_file('spam.exe'))
