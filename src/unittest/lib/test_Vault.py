import unittest
import tempfile
from unittest.mock import patch
import uuid
import configparser

from ...lib.Vault import Vault
from ...lib.Config import Config


class Test(unittest.TestCase):

    def setUp(self):
        # Set temporary files
        file_config = tempfile.NamedTemporaryFile()
        file_vault = tempfile.NamedTemporaryFile()

        # Load fake config
        c = Config(file_config.name)
        self.config = c.getConfig()

        # Load empty vault
        self.vault = Vault(self.config, file_vault.name)

        # Set a master key
        self.vault.masterKey = str(uuid.uuid4())

        # Create empty vault
        self.vault.vault = {}
        self.vault.saveVault()

    # def test_setup(self):
    #     with unittest.mock.patch('getpass.getpass', return_value=str(uuid.uuid4())):
    #         with unittest.mock.patch('src.lib.Vault.Vault.unlock', return_value=None):
    #             self.assertIsNone(self.vault.setup())

    def test_setAutoLockTimer(self):
        self.vault.setAutoLockTimer()
        self.assertIsInstance(self.vault.timer, int)

    def test_input(self):
        with unittest.mock.patch('builtins.input', return_value='my input'):
            self.assertEqual(self.vault.input('your input?'), 'my input')

    def test_unlock(self):
        # Ensure that the vault is correctly saved first
        self.vault.saveVault()

        # Try to unlock with the master key previously chosen
        with unittest.mock.patch('getpass.getpass', return_value=self.vault.masterKey):
            # False = don't load menu after unlocking
            self.assertIsNone(self.vault.unlock(False))

    def test_openVault(self):
        # Ensure that the vault is correctly saved first
        self.vault.saveVault()

        self.vault.openVault()
        self.assertIsInstance(self.vault.vault, dict)

    def test_getHash(self):
        self.assertIsInstance(self.vault.getHash(), bytes)
        self.assertEqual(len(self.vault.getHash()), 24)

    def test_addItem(self):
        self.vault.addItem(categoryId=0, name='my name',
                           login='gab@gmail.com', password='my secret', notes='some notes')
        self.assertIsInstance(self.vault.vault['secrets'], list)
        self.assertEqual(
            self.vault.vault['secrets'][0]['name'], 'my name')

    def test_all(self):
        self.vault.vault = {'secrets': {}}
        self.assertIsNone(self.vault.all())

    # def test_lock(self):
    #     with unittest.mock.patch('src.lib.Vault.Vault.unlock', return_value=None):
    #         self.assertIsNone(self.vault.lock())

    def test_quit(self):
        self.assertRaises(SystemExit, self.vault.quit)

    def test_showSecretCount(self):
        self.vault.vault = {'secrets': {}}
        self.assertIsNone(self.vault.showSecretCount())

    def test_categoryAdd(self):
        with unittest.mock.patch('builtins.input', return_value='my category'):
            self.vault.categoryAdd()
            self.assertIsInstance(self.vault.vault['categories'], list)
            self.assertEqual(
                self.vault.vault['categories'][0]['name'], 'my category')

    def test_categoriesList(self):
        self.assertIsNone(self.vault.categoriesList())

    def test_categoryIsUsed(self):
        self.assertFalse(self.vault.categoryIsUsed(12))

    def test_categoryCheckId(self):
        with unittest.mock.patch('builtins.input', return_value='my category'):
            self.vault.categoryAdd()
            self.assertIsInstance(self.vault.vault['categories'], list)

        self.assertTrue(self.vault.categoryCheckId(0))
        self.assertFalse(self.vault.categoryCheckId(12))

    def test_getSignature(self):
        self.assertEqual(self.vault.getSignature(
            'some string'), '61d034473102d7dac305902770471fd50f4c5b26f6831a56dd90b5184b3c30fc')

    def test_getVault(self):
        self.vault.vault = {'secrets': {}}
        self.assertIsInstance(self.vault.getVault(), dict)

    def test_isUnicodeSupported(self):
        self.assertIsInstance(self.vault.isUnicodeSupported(), bool)

    def test_lockPrefix(self):
        if self.vault.isUnicodeSupported():
            self.assertEqual(self.vault.lockPrefix(), u'\U0001F511  ')
        else:
            self.assertEqual(self.vault.lockPrefix(), '')
