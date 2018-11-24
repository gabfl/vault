from unittest.mock import patch
import tempfile
import json

from ..base import BaseTest
from ...views import import_export
from ...models.Secret import SecretModel
from ...models.Category import CategoryModel
from ...modules.carry import global_scope


class Test(BaseTest):

    def setUp(self):
        # Create some secrets
        secret_1 = SecretModel(name='Paypal',
                               url='https://www.paypal.com',
                               login='gab@gmail.com',
                               password='password123',
                               notes='Some notes',
                               category_id=1)
        self.session.add(secret_1)
        secret_2 = SecretModel(name='Gmail',
                               url='https://www.gmail.com',
                               login='gab@gmail.com',
                               password='password;123',
                               notes='Some notes\nsome more notes')
        self.session.add(secret_2)
        secret_3 = SecretModel(name='eBay',
                               url='https://www.ebay.com',
                               login='gab@gmail.com',
                               password='123password',
                               notes='Some notes')
        self.session.add(secret_3)

        # Add a category as well
        category_1 = CategoryModel(name='My category 1')
        self.session.add(category_1)

        self.session.commit()

    def test_import_(self):
        with patch('builtins.input', return_value='y'):
            with patch('getpass.getpass', return_value=self.secret_key):
                self.assertTrue(import_export.import_(
                    format_='json',
                    path='sample/export.json'))

    def test_import_2(self):
        self.assertRaises(ValueError, import_export.import_,
                          format_='some_invalid_format', path='/tmp/')

    def test_export_(self):
        # Create a temporary file
        file_ = tempfile.NamedTemporaryFile(delete=False)

        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertTrue(import_export.export_(
                format_='json', path=file_.name))

    def test_export_2(self):
        self.assertRaises(ValueError, import_export.export_,
                          format_='some_invalid_format', path='/tmp/')

    def test_export_to_json(self):
        # Create a temporary file
        file_ = tempfile.NamedTemporaryFile(delete=False)

        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertTrue(import_export.export_to_json(file_.name))

        # Try read the file
        with open(file_.name, mode='r') as f:
            # Get content
            content = f.read()

            # Decode content
            content = json.loads(content)

            # The content should be a list
            self.assertIsInstance(content, list)

            # Each item should be a dict
            for item in content:
                self.assertIsInstance(item, dict)

    def test_import_from_json(self):
        # Test basic import
        global_scope['enc'] = None
        with patch('builtins.input', return_value='y'):
            with patch('getpass.getpass', return_value=self.secret_key):
                self.assertTrue(import_export.import_from_json(
                    'sample/export.json'))

    def test_import_from_json_2(self):
        # Test import when vault is already unlocked (in unit test base)
        with patch('builtins.input', return_value='y'):
            self.assertTrue(import_export.import_from_json(
                'sample/export.json'))

    def test_import_from_json_3(self):
        # Test import with confirmation denied
        with patch('builtins.input', return_value='n'):
            with patch('getpass.getpass', return_value=self.secret_key):
                self.assertFalse(import_export.import_from_json(
                    'sample/export.json'))

    def test_to_table(self):
        self.assertIsInstance(import_export.to_table(
            [['name', 'url', 'login', 'password', 'notes', 'category']]), str)

    def test_to_table_2(self):
        self.assertIsInstance(import_export.to_table([]), str)
        self.assertEqual(import_export.to_table([]), 'Empty!')

    def test_read_file(self):
        # Write a temporary file
        file_ = tempfile.NamedTemporaryFile(delete=False)
        file_.write(b'Some file content')
        file_.close()

        self.assertEqual(import_export.read_file(
            file_.name), 'Some file content')

    def test_read_file_2(self):
        # Create a temporary directory
        dir_ = tempfile.TemporaryDirectory()

        self.assertRaises(SystemExit, import_export.read_file,
                          dir_.name + '/non/existent')

        # Cleanup dir
        dir_.cleanup()

    def test_save_file(self):
        # Create a temporary directory
        dir_ = tempfile.TemporaryDirectory()

        self.assertTrue(import_export.save_file(
            dir_.name + '/file', 'some content'))

        # Cleanup dir
        dir_.cleanup()

    def test_save_file_2(self):
        # Create a temporary directory
        dir_ = tempfile.TemporaryDirectory()

        self.assertFalse(import_export.save_file(
            dir_.name + '/non/existent/file', 'some content'))

        # Cleanup dir
        dir_.cleanup()

    def test_unlock(self):
        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertTrue(import_export.unlock())
