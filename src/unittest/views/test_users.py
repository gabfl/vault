from ..base import BaseTest
from ...models.base import get_session, sessions
from ...models import base
from ...models.User import UserModel
from ...views import users
from ...modules.carry import global_scope
from ...lib.Encryption import Encryption


class Test(BaseTest):

    def setUp(self):
        # Create validation key
        key_salt = global_scope['enc'].key + \
            global_scope['conf'].salt.encode()

        # Save user
        user = UserModel(key='key_validation',
                         value=global_scope['enc'].encrypt(key_salt))
        get_session().add(user)
        get_session().commit()

    def tearDown(self):
        # Truncate table
        self.session.query(UserModel).delete()
        self.session.commit()

    def test_validation_key_new(self):
        users.validation_key_new()

        # Get inserted row
        user = get_session().query(UserModel).filter(
            UserModel.key == 'key_validation').order_by(UserModel.id.desc()).first()

        # Re-create key + salt
        key_salt = global_scope['enc'].key + \
            global_scope['conf'].salt.encode()

        self.assertEqual(global_scope['enc'].decrypt(user.value), (key_salt))

    def test_validation_key_validate(self):
        self.assertTrue(users.validation_key_validate(
            self.secret_key.encode()))

    def test_validation_key_validate_2(self):
        # Testing "except exc.DatabaseError"

        # Force re-initialization of db session
        save_sessions = base.sessions
        base.sessions = {}

        # Force wrong key in Encryption class
        global_scope['enc'].key = b'some invalid key'

        self.assertFalse(users.validation_key_validate(
            b'some invalid key'))

        # Restore db sessions
        base.sessions = save_sessions

        # Restore key
        global_scope['enc'].key = self.secret_key.encode()

    def test_validation_key_validate_3(self):
        # Testing "except ValueError" for key decryption error

        self.assertFalse(users.validation_key_validate(
            b'some invalid key'))

    def test_validation_key_rekey(self):
        enc = Encryption(b'new key')
        self.assertTrue(users.validation_key_rekey(enc))

    def test_validation_key_rekey_2(self):
        # Test without a valid row in the table

        # Truncate table
        self.session.query(UserModel).delete()
        self.session.commit()

        enc = Encryption(b'new key')
        self.assertFalse(users.validation_key_rekey(enc))
