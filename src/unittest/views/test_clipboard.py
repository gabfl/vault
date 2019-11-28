from unittest.mock import patch

import pyperclip

from ..base import BaseTest
from ...views import clipboard
from ...modules.carry import global_scope


class Test(BaseTest):

    @patch.object(pyperclip, 'copy')
    def test_copy(self, patched):
        patched.return_value = None
        clipboard.copy('some string')
        self.assertEqual(clipboard.get_signature(
            'some string'), '61d034473102d7dac305902770471fd50f4c5b26f6831a56dd90b5184b3c30fc')

    @patch.object(pyperclip, 'copy')
    def test_copy_none(self, patched):
        patched.return_value = None
        assert clipboard.copy(None) is False

    @patch.object(pyperclip, 'paste')
    def test_is_changed(self, patched):
        patched.return_value = 'some string'
        clipboard.clipboard_signature = clipboard.get_signature('some string')
        self.assertFalse(clipboard.is_changed())

    @patch.object(pyperclip, 'paste')
    def test_is_changed_2(self, patched):
        patched.return_value = 'some other string'
        clipboard.clipboard_signature = clipboard.get_signature('some string')
        self.assertTrue(clipboard.is_changed())

    def test_getSignature(self):
        self.assertEqual(clipboard.get_signature(
            'some string'), '61d034473102d7dac305902770471fd50f4c5b26f6831a56dd90b5184b3c30fc')

    @patch.object(pyperclip, 'copy')
    @patch.object(pyperclip, 'paste')
    def test_wait(self, patched, patched2):
        patched.return_value = 'some string'
        patched2.return_value = 'some string'
        # Ensure we have a short wait time
        global_scope['conf'].update('clipboardTTL', '1')

        self.assertIsNone(clipboard.wait())
        self.assertEqual(clipboard.clipboard_signature, '')

    @patch.object(pyperclip, 'copy')
    @patch.object(pyperclip, 'paste')
    def test_wait_2(self, patched, patched2):
        patched.return_value = 'some other string'
        patched2.return_value = 'some string'
        # Ensure we have a short wait time
        global_scope['conf'].update('clipboardTTL', '1')

        self.assertIsNone(clipboard.wait())
        self.assertEqual(clipboard.clipboard_signature, '')

    @patch.object(pyperclip, 'copy')
    @patch.object(pyperclip, 'paste')
    def test_erase(self, patched, patched2):
        patched.return_value = 'some string'
        patched2.return_value = 'some string'
        clipboard.erase()
        self.assertEqual(clipboard.clipboard_signature, '')
