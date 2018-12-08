from unittest.mock import patch
import uuid

from ..base import BaseTest
from ...models.Secret import SecretModel
from ...lib.Encryption import Encryption
from ...modules.carry import global_scope


class Test(BaseTest):

    def setUp(self):
        # Set secret vars
        self.name = 'Vault'
        self.url = 'https://github.com/gabfl/vault'
        self.login = 'gab'
        self.password = 'some_password'
        self.notes = 'some notes'

        # Create a secret
        secret = SecretModel(name=self.name,
                             url=self.url,
                             login=self.login,
                             password=self.password,
                             notes=self.notes)
        self.session.add(secret)
        self.session.commit()

    def test_get_by_name(self):
        secret = self.session.query(
            SecretModel).filter_by(name=self.name).first()
        self.assertEqual(secret.name, self.name)
        self.assertEqual(secret.url, self.url)

    def test_repr(self):
        secret = self.session.query(SecretModel).get(1)
        print(secret)  # Required for codecov
        self.assertIsInstance(secret, object)

    def test_get_enc(self):
        secret = self.session.query(
            SecretModel).filter_by(name=self.name).first()
        self.assertIsInstance(secret.get_enc(), Encryption)

    def test_get_enc_2(self):
        with patch.dict(global_scope, {'enc': None}):
            secret = self.session.query(
                SecretModel).filter_by(name=self.name).first()
            self.assertRaises(RuntimeError, secret.get_enc)

    def test_getter_salt(self):
        secret = self.session.query(
            SecretModel).filter_by(name=self.name).first()
        self.assertIsInstance(secret.salt, bytes)

    def test_getter_password(self):
        secret = self.session.query(
            SecretModel).filter_by(name=self.name).first()
        self.assertEqual(secret.password, self.password)

    def test_getter_notes(self):
        secret = self.session.query(
            SecretModel).filter_by(name=self.name).first()
        self.assertEqual(secret.notes, self.notes)
