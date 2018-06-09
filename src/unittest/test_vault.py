import tempfile
from pathlib import Path
from unittest.mock import patch
import os
import uuid

from .base import BaseTest
from .. import vault
from ..modules import misc
from ..modules.carry import global_scope
from ..lib.Config import Config
from ..views import menu, setup


class Test(BaseTest):

    def test_get_vault_path(self):
        self.assertEqual(vault.get_vault_path('/some/path'), '/some/path')

    def test_get_vault_path_2(self):
        self.assertEqual(vault.get_vault_path(),
                         os.path.expanduser('~') + '/.vault/.secure.db')

    def test_get_config_path(self):
        self.assertEqual(vault.get_config_path('/some/path'), '/some/path')

    def test_get_config_path_2(self):
        self.assertEqual(vault.get_config_path(),
                         os.path.expanduser('~') + '/.vault/.config')

    def test_check_directory(self):
        self.assertIsInstance(vault.check_directory(
            os.path.expanduser('~') + '/.vault/.secure.db', os.path.expanduser('~') + '/.vault/.config'), bool)

    def test_check_directory_2(self):
        # Set temporary files
        file_config = tempfile.NamedTemporaryFile()
        file_vault = tempfile.NamedTemporaryFile()

        self.assertIsNone(vault.check_directory(
            file_vault.name, file_config.name))

    def test_config_update(self):
        self.assertTrue(vault.config_update(clipboard_TTL='5'))

    def test_config_update_2(self):
        self.assertTrue(vault.config_update(auto_lock_TTL='5'))

    def test_config_update_3(self):
        self.assertTrue(vault.config_update(hide_secret_TTL='5'))

    @patch.object(menu, 'menu')
    def test_initialize(self, patched):
        # Test unlock

        patched.return_value = None

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=self.secret_key):
            vault.initialize(
                global_scope['db_file'], self.conf_path.name + '/config')

    @patch.object(vault, 'erase_vault')
    def test_initialize_2(self, patched):
        # Test erase

        patched.return_value = 'patched'

        # Set temporary files
        file_vault = tempfile.NamedTemporaryFile(delete=False)
        Path(file_vault.name).touch()

        self.assertRaises(SystemExit, vault.initialize,
                          file_vault.name, self.conf_path.name + '/config', erase=True)

    def test_initialize_3(self):
        # Test re-keyi

        # Set temporary files
        file_vault = tempfile.NamedTemporaryFile(delete=False)
        Path(file_vault.name).touch()

        self.assertRaises(SystemExit, vault.initialize,
                          file_vault.name, self.conf_path.name + '/config', rekey_vault=True)

    @patch.object(vault, 'import_')
    def test_initialize_4(self, patched):
        # Test import

        patched.return_value = 'patched'

        # Set temporary files
        file_vault = tempfile.NamedTemporaryFile(delete=False)
        Path(file_vault.name).touch()

        self.assertRaises(SystemExit, vault.initialize,
                          file_vault.name, self.conf_path.name + '/config', import_items=True)

    @patch.object(vault, 'export_')
    def test_initialize_5(self, patched):
        # Test export

        patched.return_value = 'patched'

        # Set temporary files
        file_vault = tempfile.NamedTemporaryFile(delete=False)
        Path(file_vault.name).touch()

        self.assertRaises(SystemExit, vault.initialize,
                          file_vault.name, self.conf_path.name + '/config', export=True)

    @patch.object(vault.setup, 'initialize')
    @patch.object(vault, 'unlock')
    def test_initialize_6(self, patched, patched2):
        # Test export

        patched.return_value = 'patched'
        patched2.return_value = 'patched'

        # Set temporary files
        dir_ = tempfile.TemporaryDirectory()

        self.assertIsNone(vault.initialize(dir_.name + '/some/new/file',
                                           self.conf_path.name + '/config'))
