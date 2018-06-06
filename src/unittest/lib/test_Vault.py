# import tempfile
# from unittest.mock import patch
# import uuid
# import configparser

# from ..base import BaseTest
# from ...lib.Vault import Vault
# from ...lib.Config import Config
# from ...modules import misc


# class Test(BaseTest):

#     def setUp(self):
#         # Set temporary files
#         file_config = tempfile.NamedTemporaryFile()
#         file_vault = tempfile.NamedTemporaryFile()

#         # Load fake config
#         c = Config(file_config.name)
#         self.config = c.get_config()

#         # Load empty vault
#         self.vault = Vault(self.config, file_vault.name)

#         # Set a master key
#         self.vault.masterKey = str(uuid.uuid4())

#         # Create empty vault
#         self.vault.vault = {'secrets': []}
#         self.vault.saveVault()

#     def test_setAutoLockTimer(self):
#         self.vault.setAutoLockTimer()
#         self.assertIsInstance(self.vault.timer, int)

#     def test_checkAutoLockTimer(self):
#         self.vault.setAutoLockTimer()
#         self.assertIsNone(self.vault.checkAutoLockTimer())

#     def test_checkThenSetAutoLockTimer(self):
#         self.vault.setAutoLockTimer()
#         self.assertIsNone(self.vault.checkThenSetAutoLockTimer())

#     def test_input(self):
#         with patch('builtins.input', return_value='my input'):
#             self.assertEqual(self.vault.input('your input?'), 'my input')

#     def test_unlock(self):
#         # Ensure that the vault is correctly saved first
#         self.vault.saveVault()

#         # Try to unlock with the master key previously chosen
#         with patch('getpass.getpass', return_value=self.vault.masterKey):
#             # False = don't load menu after unlocking
#             self.assertIsNone(self.vault.unlock(False))

#     def test_saveVault(self):
#         self.assertTrue(self.vault.saveVault())

#     def test_openVault(self):
#         # Ensure that the vault is correctly saved first
#         self.vault.saveVault()

#         self.vault.openVault()
#         self.assertIsInstance(self.vault.vault, dict)

#     def test_getHash(self):
#         self.assertIsInstance(self.vault.getHash(), bytes)
#         self.assertEqual(len(self.vault.getHash()), 24)

#     def test_addItem(self):
#         self.vault.addItem(categoryId=0, name='my name',
#                            login='gab@gmail.com', password='my secret', notes='some notes')
#         self.assertIsInstance(self.vault.vault['secrets'], list)
#         self.assertEqual(
#             self.vault.vault['secrets'][0]['name'], 'my name')

#     def test_menu(self):
#         with patch('builtins.input', return_value='q'):
#             self.assertRaises(SystemExit, self.vault.menu)

#     @patch.object(Vault, 'itemMenu')
#     def test_get(self, patched):
#         patched.return_value = None

#         # Ensure that the vault is correctly saved first
#         self.vault.vault['secrets'].append({
#             'category': 0,
#             'name': 'some name',
#             'login': 'some login',
#             'password': 'my secret',
#             'notes': ''
#         })
#         self.vault.saveVault()

#         self.assertIsNone(self.vault.get(0))

#     def test_itemMenu(self):
#         # Set item
#         item = {
#             'category': 0,
#             'name': 'some name',
#             'login': 'some login',
#             'password': 'my secret',
#             'notes': ''
#         }

#         # Ensure that the vault is correctly saved first
#         self.vault.vault['secrets'].append(item)
#         self.vault.saveVault()

#         for command in ['s', 'b', 'q']:
#             with patch('builtins.input', return_value=command):
#                 self.assertEqual(self.vault.itemMenu(0, item), command)

#     def test_itemShowSecret(self):
#         self.vault.config['hideSecretTTL'] = '1'
#         self.assertIsNone(self.vault.itemShowSecret('some secret'))

#     def test_itemEdit(self):
#         # Set item
#         item = {
#             'category': 0,
#             'name': 'some name',
#             'login': 'some login',
#             'password': 'my secret',
#             'notes': ''
#         }

#         # Ensure that the vault is correctly saved first
#         self.vault.vault['secrets'].append(item)
#         self.vault.saveVault()

#         with patch('builtins.input', return_value='b'):
#             self.assertIsNone(self.vault.itemEdit(0, item))

#     # @patch.object(misc, 'confirm')
#     # def test_itemDelete(self, patched):
#     #     patched.return_value = True

#     #     # Set item
#     #     item = {
#     #         'category': 0,
#     #         'name': 'some name',
#     #         'login': 'some login',
#     #         'password': 'my secret',
#     #         'notes': ''
#     #     }

#     #     # Ensure that the vault is correctly saved first
#     #     self.vault.vault['secrets'].append(item)
#     #     self.vault.saveVault()

#     #     self.assertIsNone(self.vault.itemDelete(0))

#     def test_search(self):
#         for command in ['s', 'a', 'l', 'q']:
#             with patch('builtins.input', return_value=command):
#                 self.assertEqual(self.vault.search(), command)

#     def test_search_2(self):
#         with patch('builtins.input', return_value='b'):
#             self.assertIsNone(self.vault.search())

#     @patch.object(Vault, 'itemMenu')
#     def test_searchResultSelection(self, patched):
#         patched.return_value = None

#         # Ensure that the vault is correctly saved first
#         self.vault.vault['secrets'].append({
#             'category': 0,
#             'name': 'some name',
#             'login': 'some login',
#             'password': 'my secret',
#             'notes': ''
#         })
#         self.vault.saveVault()

#         with patch('builtins.input', return_value='0'):
#             self.assertIsNone(self.vault.searchResultSelection({1: 0}))

#     def test_all(self):
#         self.vault.vault = {'secrets': {}}
#         self.assertIsNone(self.vault.all())

#     @patch.object(Vault, 'unlock')
#     def test_lock(self, patched):
#         patched.return_value = None
#         self.assertIsNone(self.vault.lock())

#     def test_quit(self):
#         self.assertRaises(SystemExit, self.vault.quit)

#     def test_showSecretCount(self):
#         self.vault.vault = {'secrets': {}}
#         self.assertIsNone(self.vault.showSecretCount())

#     def test_categoriesMenu(self):
#         with patch('builtins.input', return_value='b'):
#             self.assertIsNone(self.vault.categoriesMenu())

#     def test_categoriesList(self):
#         self.assertIsNone(self.vault.categoriesList())

#     def test_categoryAdd(self):
#         with patch('builtins.input', return_value='my category'):
#             self.vault.categoryAdd()
#             self.assertIsInstance(self.vault.vault['categories'], list)
#             self.assertEqual(
#                 self.vault.vault['categories'][0]['name'], 'my category')

#     # @patch.object(misc, 'confirm')
#     # def test_categoryDelete(self, patched):
#     #     patched.return_value = True

#     #     with patch('builtins.input', return_value='my category'):
#     #         self.vault.categoryAdd()

#     #     with patch('builtins.input', return_value='0'):
#     #         self.assertIsNone(self.vault.categoryDelete())

#     # @patch.object(misc, 'confirm')
#     # def test_categoryDelete_2(self, patched):
#     #     patched.return_value = True

#     #     with patch('builtins.input', return_value='my category'):
#     #         self.vault.categoryAdd()

#     #     with patch('builtins.input', return_value='12'):
#     #         self.assertIsNone(self.vault.categoryDelete())

#     # def test_categoryIsUsed(self):
#     #     self.assertFalse(self.vault.categoryIsUsed(12))

#     @patch.object(misc, 'confirm')
#     def test_categoryRename(self, patched):
#         patched.return_value = True

#         with patch('builtins.input', return_value='my category'):
#             self.vault.categoryAdd()

#         with patch('builtins.input', return_value='new name for my category'):
#             self.assertIsNone(self.vault.categoryRename())

#     def test_categoryCheckId(self):
#         with patch('builtins.input', return_value='my category'):
#             self.vault.categoryAdd()
#             self.assertIsInstance(self.vault.vault['categories'], list)

#         self.assertTrue(self.vault.categoryCheckId(0))
#         self.assertFalse(self.vault.categoryCheckId(12))

#     def test_categoryName(self):
#         with patch('builtins.input', return_value='my category'):
#             self.vault.categoryAdd()

#         self.assertEqual(self.vault.categoryName(0), 'my category')

#     def test_categoryName_2(self):
#         with patch('builtins.input', return_value='my category'):
#             self.vault.categoryAdd()

#         self.assertEqual(self.vault.categoryName(12), 'n/a')

#     def test_getSignature(self):
#         self.assertEqual(self.vault.getSignature(
#             'some string'), '61d034473102d7dac305902770471fd50f4c5b26f6831a56dd90b5184b3c30fc')

#     @patch.object(Vault, 'clipboard')
#     @patch.object(Vault, 'isClipboardChanged')
#     def test_waitAndEraseClipboard(self, patched, patched2):
#         patched.return_value = None
#         patched.return_value = False

#         self.vault.config['clipboardTTL'] = '1'
#         self.assertIsNone(self.vault.waitAndEraseClipboard())

#     def test_changeKey(self):
#         with patch('getpass.getpass', return_value=str(uuid.uuid4())):
#             self.assertIsNone(self.vault.changeKey())

#     def test_getVault(self):
#         self.vault.vault = {'secrets': {}}
#         self.assertIsInstance(self.vault.getVault(), dict)
