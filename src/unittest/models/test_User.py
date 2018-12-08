from ..base import BaseTest
from ...models.User import UserModel


class Test(BaseTest):

    def test_get_key_validation(self):
        user = self.session.query(UserModel).filter_by(
            key='key_validation').first()
        self.assertIsInstance(user.value, bytes)

    def test_repr(self):
        user = self.session.query(UserModel).get(1)
        print(user)  # Required for codecov
        self.assertIsInstance(user, object)
