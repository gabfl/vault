
import unittest
import tempfile
from unittest.mock import patch

from ...lib import Misc


class Test(unittest.TestCase):

    def test_logo(self):
        self.assertIsNone(Misc.logo(), str)

    def test_createFolderIfMissing(self):
        with tempfile.TemporaryDirectory() as dir_:
            self.assertIsNone(Misc.createFolderIfMissing(
                dir_ + '/some/dir'))

    def test_assessIntegrity(self):
        with tempfile.NamedTemporaryFile() as file_:
            self.assertRaises(SystemExit, Misc.assessIntegrity,
                              file_.name, 'non_existent')

    def test_eraseVault(self):
        # Create fake files
        file_a = tempfile.NamedTemporaryFile()
        file_b = tempfile.NamedTemporaryFile()

        # Write in the files
        file_a.write(b'Hello world!')
        file_a.close()
        file_b.write(b'Hello world!')
        file_b.close()

        with unittest.mock.patch('src.lib.Misc.confirm', return_value=True):
            self.assertRaises(SystemExit, Misc.eraseVault,
                              file_a.name, file_b.name)

        with unittest.mock.patch('src.lib.Misc.confirm', return_value=False):
            self.assertRaises(SystemExit, Misc.eraseVault,
                              file_a.name, file_b.name)

    def test_confirm(self):
        with unittest.mock.patch('builtins.input', return_value='y'):
            self.assertTrue(Misc.confirm())
            self.assertTrue(Misc.confirm(resp=True))

        with unittest.mock.patch('builtins.input', return_value='n'):
            self.assertFalse(Misc.confirm())
            self.assertFalse(Misc.confirm(resp=True))
