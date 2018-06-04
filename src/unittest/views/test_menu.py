from unittest.mock import patch

from ..base import BaseTest
from ...models.Secret import Secret
from ...views import menu
from ...modules.carry import global_scope


class Test(BaseTest):

    def test_get_input_with_autolock(self):
        with patch('builtins.input', return_value='some input'):
            self.assertEqual(menu.get_input_with_autolock(
                non_locking_values=['a', 'b']), 'some input')

    def test_get_input_with_autolock_2(self):
        with patch('builtins.input', return_value='some input'):
            self.assertEqual(menu.get_input_with_autolock(), 'some input')

    def test_unlock(self):
        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertTrue(menu.unlock(redirect_to_menu=False))

    @patch.object(menu, 'menu')
    def test_unlock_2(self, patched):
        patched.return_value = None
        with patch('getpass.getpass', return_value=self.secret_key):
            self.assertIsNone(menu.unlock(redirect_to_menu=True))

    def test_unlock_3(self):
        with patch('getpass.getpass', return_value='wrong password'):
            self.assertRaises(SystemExit, menu.unlock)

    def test_validate_key(self):
        self.assertTrue(menu.validate_key(
            self.secret_key))

    def test_validate_key_2(self):
        self.assertFalse(menu.validate_key(
            'some invalid key'))

    def test_menu(self):
        with patch('builtins.input', return_value='q'):
            self.assertRaises(SystemExit, menu.menu)

    def test_menu_2(self):
        self.assertRaises(SystemExit, menu.menu, next_command='q')

    @patch.object(menu, 'unlock')
    def test_lock(self, patched):
        patched.return_value = None
        self.assertIsNone(menu.lock())
        self.assertIsNone(global_scope['enc'])

    def test_quit(self):
        self.assertRaises(SystemExit, menu.quit)

    def test_set_autolock_timer(self):
        menu.set_autolock_timer()
        self.assertIsInstance(menu.timer, int)

    def test_check_autolock_timer(self):
        menu.check_autolock_timer()
        self.assertIsNone(menu.check_autolock_timer())

    # @patch.object(menu, 'lock')
    # def test_check_autolock_timer_2(self, patched):
    #     patched.return_value = None
    #     menu.timer = 100
    #     self.assertTrue(menu.check_autolock_timer())

    def test_check_then_set_autolock_timer(self):
        menu.check_then_set_autolock_timer()
        self.assertIsNone(menu.check_then_set_autolock_timer())
