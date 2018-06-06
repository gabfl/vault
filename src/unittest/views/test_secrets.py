from unittest.mock import patch

import pyperclip

from ..base import BaseTest
from ...models.Secret import Secret
from ...models.Category import Category
from ...views import secrets
from ...modules.carry import global_scope


class Test(BaseTest):

    def setUp(self):
        # Create some secrets
        secret_1 = Secret(name='Paypal',
                          url='https://www.paypal.com',
                          login='gab@gmail.com',
                          password='password123',
                          notes='Some notes',
                          category_id=1)
        self.session.add(secret_1)
        secret_2 = Secret(name='Gmail',
                          url='https://www.gmail.com',
                          login='gab@gmail.com',
                          password='password;123',
                          notes='Some notes\nsome more notes')
        self.session.add(secret_2)
        secret_3 = Secret(name='eBay',
                          url='https://www.ebay.com',
                          login='gab@gmail.com',
                          password='123password',
                          notes='Some notes')
        self.session.add(secret_3)

        # Add a category as well
        category_1 = Category(name='My category 1')
        self.session.add(category_1)

        self.session.commit()

    def tearDown(self):
        self.session.query(Secret).delete()
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
            self.assertTrue(secrets.delete_input(1))

    def test_delete_confirm_2(self):
        # Confirmation denied
        with patch('builtins.input', return_value='n'):
            self.assertFalse(secrets.delete_input(1))

    def test_search(self):
        # Search with a name
        results = secrets.search('paypal')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)

    def test_search_2(self):
        # Search with a login
        results = secrets.search('gab@gmail')
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 3)

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

    def test_item_menu(self):
        with patch('builtins.input', return_value='s'):
            self.assertEqual(secrets.item_menu(secrets.get_by_id(1)), 's')

    def test_wait(self):
        # Ensure we have a short wait time
        global_scope['conf'].update('hideSecretTTL', '1')

        self.assertTrue(secrets.show_secret('some password'))
