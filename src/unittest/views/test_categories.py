from unittest.mock import patch

from ..base import BaseTest
from ...models.Category import Category
from ...models.Secret import Secret
from ...views import categories


class Test(BaseTest):

    def setUp(self):
        # Create some categories
        category_1 = Category(name='My category 1')
        self.session.add(category_1)
        category_2 = Category(name='My category 2')
        self.session.add(category_2)
        category_3 = Category(name='My category 3')
        self.session.add(category_3)
        category_4 = Category(name='My disabled category', active=0)
        self.session.add(category_4)
        self.session.commit()

    def tearDown(self):
        self.session.query(Category).delete()
        self.session.commit()

    def test_all(self):
        cats = categories.all()
        self.assertIsInstance(cats, list)
        self.assertEqual(len(cats), 3)

    def test_all_table(self):
        self.assertIsInstance(categories.all_table(), str)

    def test_all_table_2(self):
        # Empty categories
        self.session.query(Category).delete()
        self.session.commit()

        self.assertEqual(categories.all_table(), 'Empty!')

    def test_pick(self):
        with patch('builtins.input', return_value='1'):
            self.assertEqual(categories.pick(), 1)

    def test_pick_2(self):
        with patch('builtins.input', return_value='1234'):
            self.assertFalse(categories.pick())

    def test_pick_3(self):
        with patch('builtins.input', return_value=''):
            self.assertFalse(categories.pick())

    def test_exists(self):
        self.assertTrue(categories.exists(1))
        self.assertTrue(categories.exists('1'))

    def test_exists_2(self):
        self.assertFalse(categories.exists(1234))
        self.assertFalse(categories.exists('1234'))

    def test_get_name(self):
        self.assertEqual(categories.get_name(1), 'My category 1')
        self.assertEqual(categories.get_name('1'), 'My category 1')

    def test_get_name_2(self):
        self.assertEqual(categories.get_name(1234), '')
        self.assertEqual(categories.get_name('1234'), '')

    def test_get_name_3(self):
        self.assertEqual(categories.get_name(None), '')

    def test_add(self):
        self.assertTrue(categories.add('My new category'))

        cat = self.session.query(Category).filter(
            Category.name == 'My new category').first()
        self.assertEqual(cat.name, 'My new category')

    def test_add_input(self):
        with patch('builtins.input', return_value='My new category'):
            self.assertTrue(categories.add_input())

    def test_add_input_2(self):
        with patch('builtins.input', return_value=None):
            self.assertFalse(categories.add_input())

    def test_rename(self):
        # Create a category
        categories.add('My new category')
        cat = self.session.query(Category).filter(
            Category.name == 'My new category').first()

        # Rename it
        self.assertTrue(categories.rename(cat.id, 'Some new name'))
        self.assertEqual(categories.get_name(cat.id), 'Some new name')

    @patch.object(categories, 'pick')
    def test_rename_input(self, patched):
        patched.return_value = 1

        with patch('builtins.input', return_value='new name'):
            self.assertTrue(categories.rename_input())

    @patch.object(categories, 'pick')
    def test_rename_input_2(self, patched):
        patched.return_value = 1

        with patch('builtins.input', return_value=''):
            self.assertFalse(categories.rename_input())

    @patch.object(categories, 'pick')
    def test_rename_input_3(self, patched):
        patched.return_value = None

        with patch('builtins.input', return_value=''):
            self.assertFalse(categories.rename_input())

    @patch.object(categories, 'pick')
    def test_rename_input_4(self, patched):
        patched.return_value = 1234

        with patch('builtins.input', return_value='new name'):
            self.assertFalse(categories.rename_input())

    def test_rename_2(self):
        # Test with non existent category
        self.assertFalse(categories.rename(1234, 'Some new name'))

    def test_delete(self):
        # Create a category
        categories.add('My new category')
        cat = self.session.query(Category).filter(
            Category.name == 'My new category').first()

        # Rename it
        self.assertTrue(categories.delete(cat.id))
        self.assertFalse(categories.exists(cat.id))

        # Deleting it again should fail
        self.assertFalse(categories.delete(cat.id))

    def test_delete_2(self):
        # Test with non existent category
        self.assertFalse(categories.rename(1234, 'Some new name'))

    @patch.object(categories, 'pick')
    def test_delete_input(self, patched):
        patched.return_value = 1

        self.assertTrue(categories.delete_input())

    @patch.object(categories, 'pick')
    def test_delete_input_2(self, patched):
        patched.return_value = 1234

        self.assertFalse(categories.delete_input())

    @patch.object(categories, 'pick')
    def test_delete_input_3(self, patched):
        patched.return_value = ''

        self.assertFalse(categories.delete_input())

    @patch.object(categories, 'pick')
    def test_delete_input_4(self, patched):
        # It should not be possible to delete a category currently used
        patched.return_value = '1'

        # Create a secret
        secret = Secret(name='Name', url='-', login='login',
                        password='password', category_id=1)
        self.session.add(secret)
        self.session.commit()

        self.assertFalse(categories.delete_input())

    def test_is_used(self):

        # Create a secret
        secret = Secret(name='Name', url='-', login='login',
                        password='password', category_id=1)
        self.session.add(secret)
        self.session.commit()

        self.assertTrue(categories.is_used(1))
        self.assertFalse(categories.is_used(1234))
