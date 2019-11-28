from unittest.mock import patch

import pyperclip

from ..base import BaseTest
from ...models.Secret import SecretModel
from ...models.Category import CategoryModel
from ...views import secrets
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
                               login='gab2@gmail.com',
                               password='123password',
                               notes='')
        self.session.add(secret_3)

        # Add a category as well
        category_1 = CategoryModel(name='My category 1')
        self.session.add(category_1)

        self.session.commit()

    def tearDown(self):
        self.session.query(SecretModel).delete()
        self.session.commit()

    def test_all(self):
        all_secrets = secrets.all()
        self.assertIsInstance(all_secrets, list)
        self.assertEqual(len(all_secrets), 3)

    def test_to_table(self):
        self.assertIsInstance(secrets.to_table(secrets.all()), str)

    def test_to_table_2(self):
        self.assertEqual(secrets.to_table([]), 'Empty!')

    def test_count(self):
        count_secrets = secrets.count()
        self.assertIsInstance(count_secrets, int)
        self.assertEqual(count_secrets, 3)

    def test_get_by_id(self):
        self.assertEqual(secrets.get_by_id(1).name, 'Paypal')

    def test_get_names(self):
        assert secrets.get_names() == ['Paypal', 'Gmail', 'eBay']

    def test_get_top_logins(self):
        assert secrets.get_top_logins() == ['gab@gmail.com', 'gab2@gmail.com']

    def test_add(self):
        self.assertTrue(secrets.add(name='Some name'))

    def test_add_input(self):
        # Leave blank to correctly pass the notes input
        with patch('builtins.input', return_value='1'):
            with patch('getpass.getpass', return_value='some password'):
                self.assertTrue(secrets.add_input())

    def test_add_input_2(self):
        # Simulate user pressing Ctrl-C
        with patch('builtins.input', return_value=False):
            self.assertFalse(secrets.add_input())

    def test_notes_input(self):
        with patch('builtins.input', return_value='some notes'):
            self.assertEqual(secrets.notes_input(),
                             ('some notes\n' * 15).strip())

    def test_notes_input_2(self):
        with patch('builtins.input', return_value=''):
            self.assertEqual(secrets.notes_input(), '')

    def test_notes_input_3(self):
        # Simulate user pressing Ctrl-C
        with patch('builtins.input', return_value=False):
            self.assertFalse(secrets.notes_input())

    def test_delete(self):
        # Successful deletion
        self.assertTrue(secrets.delete(1))

    def test_delete_2(self):
        # Deletion of non existing secret
        self.assertFalse(secrets.delete(1234))

    def test_delete_confirm(self):
        # Successful deletion
        with patch('builtins.input', return_value='y'):
            self.assertTrue(secrets.delete_confirm(1))

    def test_delete_confirm_2(self):
        # Test with a non existent ID
        with patch('builtins.input', return_value='y'):
            self.assertFalse(secrets.delete_confirm(1234))

    def test_delete_confirm_3(self):
        # Confirmation denied
        with patch('builtins.input', return_value='n'):
            self.assertFalse(secrets.delete_confirm(1))

    def test_search(self):
        # Search with a name
        results = secrets.search('paypal')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)

    def test_search_2(self):
        # Search with a login
        results = secrets.search('gab@gmail')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)

    def test_search_3(self):
        # Search with a URL
        results = secrets.search('www.gmail.com')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)

    def test_search_dispatch(self):
        # Real int
        results = secrets.search_dispatch(1)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)

    def test_search_dispatch_2(self):
        # String is int
        results = secrets.search_dispatch('1')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)

    def test_search_dispatch_3(self):
        # Integer that does not match an actual ID
        results = secrets.search_dispatch(1234)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)

    def test_search_dispatch_4(self):
        # Keyword
        results = secrets.search_dispatch('ebay')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)

    def test_search_input(self):
        # Empty search
        with patch('builtins.input', return_value=''):
            self.assertFalse(secrets.search_input())

    def test_search_input_2(self):
        # Fat-finger prevention
        with patch('builtins.input', return_value='q'):
            self.assertEqual(secrets.search_input(), 'q')

    def test_search_input_3(self):
        # Fat-finger prevention
        with patch('builtins.input', return_value='b'):
            self.assertFalse(secrets.search_input())

    @patch.object(secrets, 'item_view')
    def test_search_input_4(self, patched):
        # Search digit
        patched.return_value = None
        with patch('builtins.input', return_value='1'):
            self.assertIsNone(secrets.search_input())

    @patch.object(secrets, 'search_results')
    def test_search_input_5(self, patched):
        # Search string
        patched.return_value = None
        with patch('builtins.input', return_value='@gmail.com'):
            self.assertIsNone(secrets.search_input())

    def test_search_input_6(self):
        # Search with no result
        with patch('builtins.input', return_value='some invalid query'):
            self.assertFalse(secrets.search_input())

    @patch.object(secrets, 'item_view')
    def test_search_results(self, patched):
        # Select valid result
        patched.return_value = None
        results = secrets.all()
        with patch('builtins.input', return_value='1'):
            self.assertIsNone(secrets.search_results(results))

    def test_search_results_2(self):
        # Type integer not corresponding to a result
        results = secrets.all()
        with patch('builtins.input', return_value='1234'):
            self.assertFalse(secrets.search_results(results))

    def test_search_results_3(self):
        # Type a string (invalid input)
        results = secrets.all()
        with patch('builtins.input', return_value='some string'):
            self.assertFalse(secrets.search_results(results))

    def test_search_results_4(self):
        # No input
        results = secrets.all()
        with patch('builtins.input', return_value=''):
            self.assertFalse(secrets.search_results(results))

    @patch.object(secrets, 'item_menu')
    def test_item_view(self, patched):
        patched.return_value = None
        result = secrets.get_by_id(1)
        self.assertIsNone(secrets.item_view(result))

    @patch.object(secrets, 'item_menu')
    def test_item_view_2(self, patched):
        # View item without notes
        patched.return_value = None
        result = secrets.get_by_id(3)
        self.assertIsNone(secrets.item_view(result))

    def test_item_menu(self):
        with patch('builtins.input', return_value='s'):
            self.assertEqual(secrets.item_menu(secrets.get_by_id(1)), 's')

    @patch.object(secrets, 'delete_confirm')
    def test_item_menu_2(self, patched):
        patched.return_value = None

        with patch('builtins.input', return_value='d'):
            self.assertIsNone(secrets.item_menu(secrets.get_by_id(1)))

    def test_item_menu_edit(self):
        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value='b'):
            self.assertIsNone(secrets.item_menu_edit(secret))

    def test_item_menu_edit_2(self):
        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value=''):
            self.assertIsNone(secrets.item_menu_edit(secret))

    @patch.object(secrets, 'edit_input')
    def test_item_menu_edit_3(self, patched):
        patched.return_value = None

        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value='c'):
            self.assertIsNone(secrets.item_menu_edit(secret))

    @patch.object(secrets, 'edit_input')
    def test_item_menu_edit_4(self, patched):
        patched.return_value = None

        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value='n'):
            self.assertIsNone(secrets.item_menu_edit(secret))

    @patch.object(secrets, 'edit_input')
    def test_item_menu_edit_5(self, patched):
        patched.return_value = None

        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value='u'):
            self.assertIsNone(secrets.item_menu_edit(secret))

    @patch.object(secrets, 'edit_input')
    def test_item_menu_edit_6(self, patched):
        patched.return_value = None

        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value='l'):
            self.assertIsNone(secrets.item_menu_edit(secret))

    @patch.object(secrets, 'edit_input')
    def test_item_menu_edit_7(self, patched):
        patched.return_value = None

        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value='p'):
            self.assertIsNone(secrets.item_menu_edit(secret))

    @patch.object(secrets, 'edit_input')
    def test_item_menu_edit_8(self, patched):
        patched.return_value = None

        secret = secrets.get_by_id(1)
        with patch('builtins.input', return_value='o'):
            self.assertIsNone(secrets.item_menu_edit(secret))

    def test_edit_input(self):
        # Edit name
        with patch('builtins.input', return_value='1'):
            self.assertTrue(secrets.edit_input(
                'category', secrets.get_by_id(1)))

        self.assertEqual(secrets.get_by_id(1).category_id, 1)

    def test_edit_input_2(self):
        # Edit category (simulate Ctr-c)
        with patch('builtins.input', return_value=False):
            self.assertFalse(secrets.edit_input(
                'category', secrets.get_by_id(1)))

    def test_edit_input_3(self):
        # Edit name
        with patch('builtins.input', return_value='new name'):
            self.assertTrue(secrets.edit_input('name', secrets.get_by_id(1)))

        self.assertEqual(secrets.get_by_id(1).name, 'new name')

    def test_edit_input_4(self):
        # Edit name (simulate Ctr-c)
        with patch('builtins.input', return_value=False):
            self.assertFalse(secrets.edit_input('name', secrets.get_by_id(1)))

    def test_edit_input_5(self):
        # Edit URL
        with patch('builtins.input', return_value='new URL'):
            self.assertTrue(secrets.edit_input('url', secrets.get_by_id(1)))

        self.assertEqual(secrets.get_by_id(1).url, 'new URL')

    def test_edit_input_6(self):
        # Edit URL (simulate Ctr-c)
        with patch('builtins.input', return_value=False):
            self.assertFalse(secrets.edit_input('url', secrets.get_by_id(1)))

    def test_edit_input_7(self):
        # Edit login
        with patch('builtins.input', return_value='new login'):
            self.assertTrue(secrets.edit_input('login', secrets.get_by_id(1)))

        self.assertEqual(secrets.get_by_id(1).login, 'new login')

    def test_edit_input_8(self):
        # Edit login (simulate Ctr-c)
        with patch('builtins.input', return_value=False):
            self.assertFalse(secrets.edit_input('login', secrets.get_by_id(1)))

    def test_edit_input_9(self):
        # Edit password
        with patch('getpass.getpass', return_value='new password'):
            self.assertTrue(secrets.edit_input(
                'password', secrets.get_by_id(1)))

        self.assertEqual(secrets.get_by_id(1).password, 'new password')

    def test_edit_input_10(self):
        # Edit password (simulate Ctr-c)
        with patch('getpass.getpass', return_value=False):
            self.assertFalse(secrets.edit_input(
                'password', secrets.get_by_id(1)))

    def test_edit_input_11(self):
        # Edit notes
        with patch('builtins.input', return_value='new notes'):
            self.assertTrue(secrets.edit_input(
                'notes', secrets.get_by_id(1)))

        self.assertEqual(secrets.get_by_id(1).notes,
                         ('new notes\n' * 15).strip())

    def test_edit_input_12(self):
        # Edit notes (simulate Ctr-c)
        with patch('builtins.input', return_value=False):
            self.assertFalse(secrets.edit_input('notes', secrets.get_by_id(1)))

    def test_edit_input_13(self):
        # Edit an invalid column: should raise a ValueError
        self.assertRaises(ValueError, secrets.edit_input,
                          'some invalid value', secrets.get_by_id(1))

    @patch.object(secrets, 'item_view')
    def test_show_secret(self, patched):
        patched.return_value = None

        # Ensure we have a short wait time
        global_scope['conf'].update('hideSecretTTL', '1')

        secret = secrets.get_by_id(1)
        self.assertIsNone(secrets.show_secret(secret))
