from ..base import BaseTest
from ...models.base import get_session
from ...models.User import User
from ...views import users
from ...modules.carry import global_scope


class Test(BaseTest):

    def test_new_validation_key(self):
        users.new_validation_key()

        # Get inserted row
        user = get_session().query(User).filter(
            User.key == 'key_validation').order_by(User.id.desc()).first()

        # Re-create key + salt
        key_salt = global_scope['enc'].key + \
            global_scope['conf'].get_config()['salt'].encode()

        self.assertEqual(global_scope['enc'].decrypt(user.value), (key_salt))

    def test_validate_validation_key(self):
        self.assertTrue(users.validate_validation_key(
            self.secret_key.encode()))

    def test_validate_validation_key_2(self):
        self.assertFalse(users.validate_validation_key(
            b'some invalid key'))
