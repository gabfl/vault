import tempfile
from unittest.mock import patch
import os
import uuid

from .base import BaseTest
from .. import vault
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
        # Use a temporary dir to test the config
        dir_ = tempfile.TemporaryDirectory()

        # Load config
        c = Config(dir_.name + '.config')
        c.getConfig()

        self.assertTrue(vault.config_update(c, clipboard_TTL='5'))

        # Cleanup temporary directory
        dir_.cleanup()

    def test_config_update_2(self):
        # Use a temporary dir to test the config
        dir_ = tempfile.TemporaryDirectory()

        # Load config
        c = Config(dir_.name + '.config')
        c.getConfig()

        self.assertTrue(vault.config_update(c, auto_lock_TTL='5'))

        # Cleanup temporary directory
        dir_.cleanup()

    def test_config_update_3(self):
        # Use a temporary dir to test the config
        dir_ = tempfile.TemporaryDirectory()

        # Load config
        c = Config(dir_.name + '.config')
        c.getConfig()

        self.assertTrue(vault.config_update(c, hide_secret_TTL='5'))

        # Cleanup temporary directory
        dir_.cleanup()

    @patch.object(VaultClass, 'menu')
    def test_initialize(self, patched):
        patched.return_value = None

        # Set temporary files
        file_config = tempfile.NamedTemporaryFile()
        file_vault = tempfile.NamedTemporaryFile()

        # Load fake config
        c = Config(file_config.name)
        c.setDefaultConfigFile()
        config = c.getConfig()

        # Load empty vault
        v = VaultClass(config, file_vault.name)

        # Set a master key
        v.masterKey = str(uuid.uuid4())

        # Create empty vault
        v.vault = {'secrets': []}

        # Ensure that the vault is correctly saved first
        v.saveVault()

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=v.masterKey):
            vault.initialize(file_vault.name, file_config.name)
