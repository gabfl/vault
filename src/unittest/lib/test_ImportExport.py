import tempfile
from unittest.mock import patch
import uuid
import pickle
import json

from ..base import BaseTest
from ...lib.ImportExport import ImportExport
from ...lib.Vault import Vault
from ...lib.Config import Config


class Test(BaseTest):

    def setUp(self):
        # Set temporary files
        file_import_export = tempfile.NamedTemporaryFile()
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
        self.vault.vault = {'secrets': []}

        # Load ImportExport
        self.ie = ImportExport(
            vault=self.vault, path=file_import_export.name, fileFormat='json')

    def test_importItems(self):
        self.ie.fileFormat = 'invalid'
        self.assertRaises(ValueError, self.ie.importItems)

    def test_export(self):
        self.ie.fileFormat = 'invalid'
        self.assertRaises(ValueError, self.ie.export)

    def test_importFromJson(self):
        # Ensure that the vault is correctly saved first
        self.vault.vault['secrets'].append({
            'category': 0,
            'name': 'some name',
            'login': 'some login',
            'password': 'my secret',
            'notes': ''
        })
        self.vault.saveVault()

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=self.vault.masterKey):
            self.assertRaises(SystemExit, self.ie.exportToJson)
            # Import
            with patch('builtins.input', return_value='y'):
                self.assertRaises(SystemExit, self.ie.importFromJson)

        # Verify vault content
        self.assertIsInstance(self.vault.vault['secrets'], list)
        self.assertEqual(self.vault.vault['secrets'][0]['name'], 'some name')

    def test_importFromNative(self):
        # Ensure that the vault is correctly saved first
        self.vault.vault['secrets'].append({
            'category': 0,
            'name': 'some name',
            'login': 'some login',
            'password': 'my secret',
            'notes': ''
        })
        self.vault.saveVault()

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=self.vault.masterKey):
            self.assertRaises(SystemExit, self.ie.exportToNative)
            # Import
            with patch('builtins.input', return_value='y'):
                self.assertRaises(SystemExit, self.ie.importFromNative)

        # Verify vault content
        self.assertIsInstance(self.vault.vault['secrets'], list)
        self.assertEqual(self.vault.vault['secrets'][0]['name'], 'some name')

    def test_exportToJson(self):
        # Ensure that the vault is correctly saved first
        self.vault.vault['secrets'].append({
            'category': 0,
            'name': 'some name',
            'login': 'some login',
            'password': 'my secret',
            'notes': ''
        })
        self.vault.saveVault()

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=self.vault.masterKey):
            self.assertRaises(SystemExit, self.ie.exportToJson)

        # Json decode and validate the content
        content = self.ie.readFile()
        content = json.loads(content)
        self.assertIsInstance(content, list)
        self.assertEqual(content[0]['name'], 'some name')

    def test_exportToNative(self):
        # Ensure that the vault is correctly saved first
        self.vault.vault['secrets'].append({
            'category': 0,
            'name': 'some name',
            'login': 'some login',
            'password': 'my secret',
            'notes': ''
        })
        self.vault.saveVault()

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=self.vault.masterKey):
            self.assertRaises(SystemExit, self.ie.exportToNative)

        # Unpickle and validate the content
        content = self.ie.readFile('rb')
        content = pickle.loads(content)
        self.assertIsInstance(content['secrets'], list)
        self.assertEqual(content['secrets'][0]['name'], 'some name')

    def test_readFile(self):
        self.ie.saveFile('some content')
        self.assertEqual(self.ie.readFile(), 'some content')

    def test_saveFile(self):
        self.assertIsNone(self.ie.saveFile('some content'))

    def test_unlockVault(self):
        # Ensure that the vault is correctly saved first
        self.vault.saveVault()

        # Try to unlock with the master key previously chosen
        with patch('getpass.getpass', return_value=self.vault.masterKey):
            self.assertIsNone(self.ie.unlockVault())

    def test_checkEmptyVault(self):
        self.assertRaises(ValueError, self.ie.checkEmptyVault)
