from unittest.mock import patch
import uuid

from ..base import BaseTest
from ...views import setup
from ...models.base import get_session
from ...models.User import UserModel
from ...modules.carry import global_scope


class Test(BaseTest):

    def test_setup(self):
        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertTrue(setup.initialize(self.config.salt))

    def test_create_db(self):
        self.assertTrue(setup.create_db())

    def test_get_key_input(self):
        input_ = str(uuid.uuid4())

        with patch('getpass.getpass', return_value=input_):
            self.assertEqual(setup.get_key_input(), input_)

    def test_get_key_input_2(self):
        with patch('getpass.getpass', return_value='abc'):
            self.assertFalse(setup.get_key_input())

    def test_is_key_valid(self):
        self.assertTrue(setup.is_key_valid(
            'some_valid_key_123'))

    def test_is_key_valid_2(self):
        self.assertFalse(setup.is_key_valid('abc'))

    def test_check_key_and_repeat(self):
        self.assertTrue(setup.check_key_and_repeat(
            'some_valid_key_123', 'some_valid_key_123'))

    def test_check_key_and_repeat_2(self):
        self.assertFalse(setup.check_key_and_repeat(
            'some_valid_key_123', 'some_valid_key_123456'))
