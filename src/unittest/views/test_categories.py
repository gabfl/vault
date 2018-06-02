import tempfile

from sqlalchemy.orm import Session

from ..base import BaseTest
from ...models.Category import Category
from ...models.Secret import Secret
from ...views import categories


class Test(BaseTest):

    def setUp(self):
        # Create some categories
        category_1 = Category(name='My category 1', active=1)
        self.session.add(category_1)
        category_2 = Category(name='My category 2', active=1)
        self.session.add(category_2)
        category_3 = Category(name='My category 3', active=1)
        self.session.add(category_3)
        category_4 = Category(name='My disabled category', active=0)
        self.session.add(category_4)
        self.session.commit()

    def tearDown(self):
        self.session.query(Category).delete()

    def test_local_session(self):
        self.assertIsInstance(categories.local_session(), Session)

    def test_local_session_2(self):
        categories.local_session()
        self.assertIsInstance(categories.session, Session)

    def test_all(self):
        cats = categories.all()
        self.assertIsInstance(cats, list)
        self.assertEqual(len(cats), 3)

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
        self.assertFalse(categories.get_name(1234))
        self.assertFalse(categories.get_name('1234'))

    def test_add(self):
        self.assertTrue(categories.add('My new category'))

        cat = self.session.query(Category).filter(
            Category.name == 'My new category').first()
        self.assertEqual(cat.name, 'My new category')

    def test_rename(self):
        # Create a category
        categories.add('My new category')
        cat = self.session.query(Category).filter(
            Category.name == 'My new category').first()

        # Rename it
        self.assertTrue(categories.rename(cat.id, 'Some new name'))
        self.assertEqual(categories.get_name(cat.id), 'Some new name')

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

    def test_is_used(self):

        # Create a secret
        secret = Secret(name='Name', url='-', login='login',
                        password='password', category_id=1)
        self.session.add(secret)
        self.session.commit()

        self.assertTrue(categories.is_used(1))
        self.assertFalse(categories.is_used(1234))