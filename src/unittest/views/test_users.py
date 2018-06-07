from ..base import BaseTest
from ...models.base import get_session, sessions
from ...models import base
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
            global_scope['conf'].salt.encode()

        self.assertEqual(global_scope['enc'].decrypt(user.value), (key_salt))

    def test_validate_validation_key(self):
        self.assertTrue(users.validate_validation_key(
            self.secret_key.encode()))

    def test_validate_validation_key_2(self):
        # Testing "except exc.DatabaseError"

        # Force re-initialization of db session
        base.sessions = {}

        # Force wrong key in Encryption class
        global_scope['enc'].key = b'some invalid key'

        self.assertFalse(users.validate_validation_key(
            b'some invalid key'))

    def test_validate_validation_key_3(self):
        # Testing "except ValueError" for key decryption error

        self.assertFalse(users.validate_validation_key(
            b'some invalid key'))
