
import unittest
import os

from .. import vault


class Test(unittest.TestCase):

    def test_getVaultPath(self):
        self.assertEqual(vault.getVaultPath('/some/path'), '/some/path')

    def test_getVaultPath_2(self):
        self.assertEqual(vault.getVaultPath(),
                         os.path.expanduser('~') + '/.vault/.secure')

    def test_getConfigPath(self):
        self.assertEqual(vault.getConfigPath('/some/path'), '/some/path')

    def test_getConfigPath_2(self):
        self.assertEqual(vault.getConfigPath(),
                         os.path.expanduser('~') + '/.vault/.config')
