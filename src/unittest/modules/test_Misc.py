
import unittest
import tempfile
from unittest.mock import patch

from ...modules import Misc


class Test(unittest.TestCase):

    def test_logo(self):
        self.assertIsNone(Misc.logo(), str)

    def test_create_directory_if_missing(self):
        # When the folder exists
        with tempfile.TemporaryDirectory() as dir_:
            self.assertIsNone(Misc.create_directory_if_missing(
                dir_))

    def test_create_directory_if_missing_2(self):
        # When the folder is missing
        with tempfile.TemporaryDirectory() as dir_:
            self.assertIsNone(Misc.create_directory_if_missing(
                dir_ + '/some/dir'))

    def test_create_directory_if_missing_3(self):
        # Test invalid path
        with tempfile.TemporaryDirectory() as dir_:
            self.assertRaises(
                SystemExit, Misc.create_directory_if_missing, '\0')

    def test_assess_integrity(self):
        with tempfile.NamedTemporaryFile() as file_:
            self.assertRaises(SystemExit, Misc.assess_integrity,
                              file_.name, 'non_existent')

    def test_erase_vault(self):
        # Create fake files
        file_a = tempfile.NamedTemporaryFile()
        file_b = tempfile.NamedTemporaryFile()

        # Write in the files
        file_a.write(b'Hello world!')
        file_a.close()
        file_b.write(b'Hello world!')
        file_b.close()

        with unittest.mock.patch('src.modules.Misc.confirm', return_value=True):
            self.assertRaises(SystemExit, Misc.erase_vault,
                              file_a.name, file_b.name)

        with unittest.mock.patch('src.modules.Misc.confirm', return_value=False):
            self.assertRaises(SystemExit, Misc.erase_vault,
                              file_a.name, file_b.name)

    def test_erase_vault_2(self):
        # Test with non existent files

        # Create fake files
        file_a = tempfile.NamedTemporaryFile()
        file_b = tempfile.NamedTemporaryFile()

        with unittest.mock.patch('src.modules.Misc.confirm', return_value=True):
            self.assertRaises(SystemExit, Misc.erase_vault,
                              file_a.name, file_b.name)

        with unittest.mock.patch('src.modules.Misc.confirm', return_value=False):
            self.assertRaises(SystemExit, Misc.erase_vault,
                              file_a.name, file_b.name)

    def test_confirm(self):
        with unittest.mock.patch('builtins.input', return_value='y'):
            self.assertTrue(Misc.confirm())
            self.assertTrue(Misc.confirm(resp=True))

    def test_confirm_2(self):
        with unittest.mock.patch('builtins.input', return_value='n'):
            self.assertFalse(Misc.confirm())
            self.assertFalse(Misc.confirm(resp=True))

    def test_confirm_3(self):
        # Test empty return
        with unittest.mock.patch('builtins.input', return_value=''):
            self.assertTrue(Misc.confirm(resp=True))
