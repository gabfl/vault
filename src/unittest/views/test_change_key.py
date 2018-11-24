from unittest.mock import patch

from sqlalchemy import engine
from sqlalchemy.orm import Session

from ..base import BaseTest
from ...views import change_key
from ...modules.carry import global_scope
from ...lib.Encryption import Encryption
from ...models.Secret import SecretModel
from ...models.User import UserModel


class Test(BaseTest):

    def setUp(self):
        # Set instances of Encryption for the current and the new key
        change_key.enc_current = global_scope['enc']
        # Forcing same key to not invalidate the db for further tests
        change_key.enc_new = Encryption(global_scope['enc'].key)

        # Create some secrets
        secret_1 = SecretModel(name='Paypal',
                               url='https://www.paypal.com',
                               login='gab@gmail.com',
                               password='password123',
                               notes='Some notes')
        self.session.add(secret_1)
        secret_2 = SecretModel(name='Gmail',
                               url='https://www.gmail.com',
                               login='gab@gmail.com',
                               password='password;123',
                               notes='Some notes\nsome more notes')
        self.session.add(secret_2)
        secret_3 = SecretModel(name='eBay',
                               url='https://www.ebay.com',
                               login='gab@gmail.com',
                               password='123password',
                               notes='')
        self.session.add(secret_3)

        # Create validation key
        key_salt = global_scope['enc'].key + \
            global_scope['conf'].salt.encode()

        # Save user
        user = UserModel(key='key_validation',
                         value=global_scope['enc'].encrypt(key_salt))
        self.session.add(user)

        self.session.commit()

    def tearDown(self):
        # Truncate users table
        self.session.query(UserModel).delete()
        self.session.commit()

    def test_rekey(self):
        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertTrue(change_key.rekey())

    @patch.object(change_key, 'get_key_input')
    def test_rekey_2(self, patched):
        patched.return_value = False

        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertFalse(change_key.rekey())

    def test_rekey_secrets(self):
        self.assertTrue(change_key.rekey_secrets())

    def test_rekey_validation_key(self):
        self.assertTrue(change_key.rekey_validation_key())

    # def test_rekey_db(self):
    #     self.assertTrue(change_key.rekey_db())

    def test_unlock(self):
        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertTrue(change_key.unlock())
