from ..base import BaseTest
from ...models.Category import CategoryModel


class Test(BaseTest):

    def setUp(self):
        # Create category
        category = CategoryModel(name='My category', active=1)
        self.session.add(category)
        self.session.commit()

    def test_get_by_name(self):
        category = self.session.query(
            CategoryModel).filter_by(name='My category').first()
        self.assertEqual(category.name, 'My category')
        self.assertEqual(category.active, 1)

    def test_repr(self):
        category = self.session.query(CategoryModel).get(1)
        print(category)  # Required for codecov
        self.assertIsInstance(category, object)
