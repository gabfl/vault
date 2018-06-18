import tempfile
from unittest.mock import patch

from ..base import BaseTest
from ...modules import misc


class Test(BaseTest):

    def test_logo(self):
        self.assertIsNone(misc.logo())

    def test_logo_small(self):
        self.assertIsNone(misc.logo_small())

    def test_create_directory_if_missing(self):
        # When the folder exists
        with tempfile.TemporaryDirectory() as dir_:
            self.assertFalse(misc.create_directory_if_missing(
                dir_))

    def test_create_directory_if_missing_2(self):
        # When the folder is missing
        with tempfile.TemporaryDirectory() as dir_:
            self.assertTrue(misc.create_directory_if_missing(
                dir_ + '/some/dir'))

    def test_create_directory_if_missing_3(self):
        # Test invalid path
        with tempfile.TemporaryDirectory() as dir_:
            self.assertRaises(
                SystemExit, misc.create_directory_if_missing, '\0')

    def test_assess_integrity(self):
        with tempfile.NamedTemporaryFile() as file_:
            self.assertRaises(SystemExit, misc.assess_integrity,
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

        with patch('src.modules.misc.confirm', return_value=True):
            self.assertRaises(SystemExit, misc.erase_vault,
                              file_a.name, file_b.name)

        with patch('src.modules.misc.confirm', return_value=False):
            self.assertRaises(SystemExit, misc.erase_vault,
                              file_a.name, file_b.name)

    def test_erase_vault_2(self):
        # Test with non existent files

        # Create fake files
        file_a = tempfile.NamedTemporaryFile()
        file_b = tempfile.NamedTemporaryFile()

        with patch('src.modules.misc.confirm', return_value=True):
            self.assertRaises(SystemExit, misc.erase_vault,
                              file_a.name + '/non/existent', file_b.name + '/non/existent')

        with patch('src.modules.misc.confirm', return_value=False):
            self.assertRaises(SystemExit, misc.erase_vault,
                              file_a.name + '/non/existent', file_b.name + '/non/existent')

    def test_confirm(self):
        with patch('builtins.input', return_value='y'):
            self.assertTrue(misc.confirm())
            self.assertTrue(misc.confirm(resp=True))

    def test_confirm_2(self):
        with patch('builtins.input', return_value='n'):
            self.assertFalse(misc.confirm())
            self.assertFalse(misc.confirm(resp=True))

    def test_confirm_3(self):
        # Test empty return
        with patch('builtins.input', return_value=''):
            self.assertTrue(misc.confirm(resp=True))

    def test_is_unicode_supported(self):
        self.assertIsInstance(misc.is_unicode_supported(), bool)

    def test_lock_prefix(self):
        if misc.is_unicode_supported():
            self.assertEqual(misc.lock_prefix(), u'\U0001F511  ')
        else:
            self.assertEqual(misc.lock_prefix(), '')

    def test_clear_screen(self):
        self.assertTrue(misc.clear_screen())
