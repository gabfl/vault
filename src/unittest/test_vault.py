
import unittest
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

    def test_getVaultPath(self):
        self.assertEqual(vault.getVaultPath('/some/path'), '/some/path')

    def test_getVaultPath_2(self):
        self.assertEqual(vault.getVaultPath(),
                         os.path.expanduser('~') + '/.vault/.secure')

    def test_getConfigPath(self):
        self.assertEqual(vault.getConfigPath('/some/path'), '/some/path')

    def test_getConfigPath_2(self):
        self.assertEqual(vault.getConfigPath(),
                         os.path.expanduser('~') + '/.vault/.config')

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
        with unittest.mock.patch('getpass.getpass', return_value=v.masterKey):
            vault.initialize(file_vault.name, file_config.name)
