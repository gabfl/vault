from unittest.mock import patch
import tempfile
from shutil import copyfile

from ..base import BaseTest
from ...views import migration
from ...lib.Config import Config


class Test(BaseTest):

    config_path_to_copy = 'src/unittest/assets/migration/legacy-config'
    vault_path = 'src/unittest/assets/migration/legacy-vault'
    legacy_password = 'password123'

    def setUp(self):
        # Copy config file to a temporary file
        self.config_path = tempfile.NamedTemporaryFile(delete=False)
        copyfile(self.config_path_to_copy, self.config_path.name)

    def test_migrate(self):
        # Successful migration
        file_ = tempfile.NamedTemporaryFile(delete=False)

        with patch('builtins.input', return_value='y'):
            with patch('getpass.getpass', return_value=self.legacy_password):
                self.assertTrue(migration.migrate(vault_path=self.vault_path,
                                                  config_path=self.config_path.name,
                                                  new_vault_path=file_.name))

    def test_migrate_2(self):
        # Migration with confirmation denied
        file_ = tempfile.NamedTemporaryFile(delete=False)

        with patch('builtins.input', return_value='n'):
            with patch('getpass.getpass', return_value=self.legacy_password):
                self.assertFalse(migration.migrate(vault_path=self.vault_path,
                                                   config_path=self.config_path.name,
                                                   new_vault_path=file_.name))

    def test_migrate_3(self):
        with patch('getpass.getpass', return_value='some invalid password'):
            self.assertRaises(SystemExit, migration.migrate,
                              vault_path=self.vault_path, config_path=self.config_path.name)

    def update_config(self):
        migration.update_config()
        self.assertEqual(migration.config.version, '2.00')
        self.assertEqual(migration.config.encrypteddb, True)

    def test_unlock(self):
        vault_content = migration.unlock(self.vault_path, self.legacy_password)
        self.assertIsInstance(vault_content, dict)
        self.assertIsInstance(vault_content['secrets'], list)
        self.assertIsInstance(vault_content['categories'], list)

    def test_get_hash(self):
        migration.config = Config(self.config_path.name)
        self.assertEqual(migration.get_hash(
            self.legacy_password), b'\xd3\xbe[{\xad6k^|\xd7\xbe\x9f\xd5\xef7o\xd7\xbbq\xce\xf7\xe9\xb7x')

    def test_prepare_items(self):
        vault_content = migration.unlock(self.vault_path, self.legacy_password)
        prepared = migration.prepare_items(
            vault_content['secrets'], vault_content['categories'])

        # The result should be a list
        self.assertIsInstance(prepared, list)

        # Loop thru items to check them
        for item in prepared:
            self.assertIsInstance(item, dict)
            self.assertIsInstance(item['name'], str)
            self.assertIsNone(item['url'])
            self.assertIsInstance(item['login'], str)
            self.assertIsInstance(item['password'], str)
            self.assertIsInstance(item['notes'], str)
            self.assertTrue(item['category'] is None or isinstance(
                item['category'], str))

    def test_get_category_name(self):
        # With valid ID
        self.assertEqual(migration.get_category_name(id_=0, categories=[
            {'name': 'Business', 'active': True}, {'name': 'Perso', 'active': True}]), 'Business')

    def test_get_category_name_2(self):
        # With invalid category
        self.assertIsNone(migration.get_category_name(id_=1, categories=[
            {'name': 'Business', 'active': True}, {'name': 'Perso', 'active': False}]))

    def test_get_category_name_3(self):
        # Without an ID
        self.assertIsNone(migration.get_category_name(id_=None, categories=[
                          {'name': 'Business', 'active': True}, {'name': 'Perso', 'active': True}]))
