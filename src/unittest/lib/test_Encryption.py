import uuid

from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto import Random as CryptoRandom

from ..base import BaseTest
from ...lib.Encryption import Encryption


class Test(BaseTest):

    def setUp(self):
        # Generate a fake key
        self.key = str(uuid.uuid4()).encode()

        self.enc2 = Encryption(self.key)

    def test_digest_key(self):
        dk = self.enc2.digest_key()
        self.assertIsInstance(dk, bytes)
        self.assertEqual(len(dk), 32)

    def test_digest_key_2(self):
        salt = self.enc2.gen_salt()
        self.enc2.set_salt(salt)
        dk = self.enc2.digest_key()
        self.assertIsInstance(dk, bytes)
        self.assertEqual(len(dk), 32)

    def test_get_aes(self):
        IV = CryptoRandom.new().read(AES.block_size)
        self.assertIsInstance(self.enc2.get_aes(IV), Cipher._mode_cbc.CbcMode)

    def test_gen_salt(self):
        salt = self.enc2.gen_salt()
        self.assertIsInstance(salt, bytes)
        self.assertTrue(len(salt) > 0)
        self.assertEqual(self.enc2.salted_key, salt + self.key)

    def test_gen_salt_2(self):
        salt = self.enc2.gen_salt(False)
        self.assertIsInstance(salt, bytes)
        self.assertTrue(len(salt) > 0)

    def test_set_salt(self):
        salt = self.enc2.gen_salt()
        self.assertEqual(self.enc2.salted_key, salt + self.key)

    def test_encrypt(self):
        secret_string = b'my secret string'
        encrypted = self.enc2.encrypt(secret_string)
        self.assertIsInstance(encrypted, bytes)
        self.assertTrue(len(encrypted) > 0)

    def test_encrypt_2(self):
        secret_string = b'my secret string'
        salt = self.enc2.gen_salt()
        encrypted = self.enc2.encrypt(secret_string)
        self.assertIsInstance(encrypted, bytes)
        self.assertTrue(len(encrypted) > 0)

    def test_decrypt(self):
        secret_string = b'my secret string'
        encrypted = self.enc2.encrypt(secret_string)
        self.assertEqual(self.enc2.decrypt(encrypted), secret_string)

    def test_decrypt_2(self):
        secret_string = b'my secret string'
        salt = self.enc2.gen_salt()
        encrypted = self.enc2.encrypt(secret_string)
        self.enc2.set_salt(salt)
        self.assertEqual(self.enc2.decrypt(encrypted), secret_string)

    def test_decrypt_3(self):
        # Test encrypting with a salt but decrypting without the salt
        secret_string = b'my secret string'
        salt = self.enc2.gen_salt()
        self.enc2.set_salt(salt)
        encrypted = self.enc2.encrypt(secret_string)
        self.assertRaises(ValueError, self.enc2.decrypt, encrypted)
