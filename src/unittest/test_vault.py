import tempfile
from pathlib import Path
from unittest.mock import patch
import os
import uuid

from .base import BaseTest
from .. import vault
from ..modules import misc
from ..lib.ImportExport import ImportExport
from ..lib.Vault import Vault as VaultClass
from ..lib.Config import Config


class Test(BaseTest):

    def test_get_vault_path(self):
        self.assertEqual(vault.get_vault_path('/some/path'), '/some/path')

    def test_get_vault_path_2(self):
        self.assertEqual(vault.get_vault_path(),
                         os.path.expanduser('~') + '/.vault/.secure')

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

    @patch.object(VaultClass, 'menu')
    def test_initialize(self, patched):
        patched.return_value = None

        # Set temporary files
        file_vault = tempfile.NamedTemporaryFile()

        # Load empty vault
        v = VaultClass(self.config, file_vault.name)

        # Set a master key
        v.masterKey = str(uuid.uuid4())

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=v.masterKey):
            vault.initialize(file_vault.name, self.conf_path.name + '/config')

    @patch.object(misc, 'erase_vault')
    @patch.object(misc, 'confirm')
    def test_initialize_2(self, patched, patched2):
        patched.return_value = 'patched'
        patched2.return_value = True

        # Set temporary files
        file_vault = tempfile.NamedTemporaryFile(delete=False)
        Path(file_vault.name).touch()

        self.assertRaises(SystemExit, vault.initialize,
                          file_vault.name, self.conf_path.name + '/config', erase=True)
