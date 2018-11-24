from unittest.mock import patch

from ..base import BaseTest
from ...models.Secret import SecretModel
from ...views import menu
from ...modules.carry import global_scope


class Test(BaseTest):

    def setUp(self):
        # Preserve enc to restore it on tear down
        self.enc_save = global_scope['enc']

    def tearDown(self):
        # restore enc in global scope
        global_scope['enc'] = self.enc_save

    def test_get_input(self):
        with patch('builtins.input', return_value='some input'):
            self.assertEqual(menu.get_input(), 'some input')

    def test_get_input_2(self):
        with patch('getpass.getpass', return_value='some secure input'):
            self.assertEqual(menu.get_input(secure=True), 'some secure input')

    def test_get_input_3(self):
        with patch('builtins.input', return_value='SOME INPUT'):
            self.assertEqual(menu.get_input(lowercase=True), 'some input')

    def test_get_input_4(self):
        with patch('builtins.input', return_value='some input'):
            self.assertEqual(menu.get_input(
                non_locking_values=['a', 'b', 'c']), 'some input')

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

    def test_unlock_4(self):
        # Simulate user pressing Ctrl-C
        with patch('getpass.getpass', return_value=False):
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

    # @patch.object(menu, 'menu')
    # def test_check_autolock_timer_2(self, patched):
    #     patched.return_value = None
    #     with patch('getpass.getpass', return_value=self.secret_key):
    #         menu.timer = 100
    #         self.assertIsNone(menu.check_autolock_timer())

    def test_check_then_set_autolock_timer(self):
        menu.check_then_set_autolock_timer()
        self.assertIsNone(menu.check_then_set_autolock_timer())
