from ..base import BaseTest
from ...models.Secret import Secret
from ...models.Category import Category
from ...views import secrets


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

    def test_all_table(self):
        all_secrets_table = secrets.all_table()
        self.assertIsInstance(all_secrets_table, str)

    def test_all_table_2(self):
        # Empty secrets
        self.session.query(Secret).delete()
        self.session.commit()

        self.assertEqual(secrets.all_table(), 'Empty!')

    def test_count(self):
        count_secrets = secrets.count()
        self.assertIsInstance(count_secrets, int)
        self.assertEqual(count_secrets, 3)
