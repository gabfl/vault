
import getpass
import json
import base64
import time
import sys
import os

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import pyperclip
from passwordgenerator import pwgenerator


class Vault:

    config = None  # Will hold user configuration
    vaultPath = None  # Vault file location
    vault = None  # Vault content once decrypted
    timer = None  # Set a timer to autolock the vault
    clipboardSignature = None  # Hash of clipboard item
    masterKey = None  # Master key

    def __init__(self, config, vaultPath):
        self.config = config
        self.vaultPath = vaultPath

    def setup(self):
        """
            Master key setup
        """

        print('Welcome to Vault. Please choose a secure secret key.')
        print()
        while True:
            try:
                self.masterKey = getpass.getpass(
                    self.lockPrefix() + 'Please choose a master key:')
                masterKeyRepeat = getpass.getpass(
                    self.lockPrefix() + 'Please confirm your master key:')
                break
            except KeyboardInterrupt as e:
                # If the user presses `Ctrl`+`c`, exit the program
                print()
                sys.exit()
            except Exception as e:  # Other Exception
                print()
                pass

        if len(self.masterKey) < 8:
            print()
            print('The master key should be at least 8 characters. Please try again!')
            print()
            # Try again
            self.setup()
        elif self.masterKey == masterKeyRepeat:
            # Create empty vault
            self.vault = {}
            self.saveVault()
            print()
            print("Your vault has been created and encrypted with your master key.")
            print("Your unique salt is: %s " % (self.config['salt']))
            print(
                "Write it down. If you lose your config file you will need it to unlock your vault.")
            self.unlock()
        else:
            print()
            print('The master key does not match its confirmation. Please try again!')
            print()
            # Try again
            self.setup()

    def setAutoLockTimer(self):
        """
            Set auto lock timer
        """

        self.timer = int(time.time())

    def checkAutoLockTimer(self):
        """
            Check auto lock timer and lock the vault if necessary
        """

        if self.timer and int(time.time()) > self.timer + int(self.config['autoLockTTL']):
            print()
            print("The vault has been locked due to inactivity.")
            self.lock()

    def checkThenSetAutoLockTimer(self):
        """
            Check auto lock timer and lock the vault if necessary, then set it again
        """

        self.checkAutoLockTimer()
        self.setAutoLockTimer()

    def input(self, string, nonLockingValues=[]):
        """
            Ask for user input and check auto lock timer before returning the value
        """

        # Get user input
        i = input(string)

        # Check the timer
        if i not in nonLockingValues:  # Except if the user input is non eligible for vault locking
            self.checkAutoLockTimer()

        # Return input
        return i

    def unlock(self, showMenu=True, tentative=1):
        """
            Asking the user for his master key and trying to unlock the vault
        """

        # Get master key
        while True:
            try:
                print()
                self.masterKey = getpass.getpass(
                    self.lockPrefix() + 'Please enter your master key:')
                break
            except KeyboardInterrupt as e:
                # If the user presses `Ctrl`+`c`, exit the program
                print()
                sys.exit()
            except Exception as e:  # Other Exception
                pass

        try:
            self.openVault()  # Unlock vault
        except Exception as e:
            if tentative >= 3:
                # Stop trying after 3 attempts
                print('Vault cannot be opened.')
                print()
                sys.exit()
            else:
                # Try again
                print('Master key is incorrect. Please try again!')
                self.unlock(showMenu, tentative + 1)

        if showMenu:
            # Show secret count
            self.showSecretCount()

            # Print vault content (for debug purpose)
            # print(json.dumps(self.vault, sort_keys=True, indent=4, separators=(',', ': ')))

            self.menu()

    def saveVault(self):
        """
            Save vault
        """

        cipher = AES.new(self.getHash(), AES.MODE_EAX)
        data = str.encode(json.dumps(self.vault))
        ciphertext, tag = cipher.encrypt_and_digest(data)

        f = open(self.vaultPath, "wb")
        try:
            [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
        finally:
            f.close()
        os.chmod(self.vaultPath, 0o600)

        return True

    def openVault(self):
        """"
            Open the vault with the master key
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        f = open(self.vaultPath, "rb")
        try:
            nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
        finally:
            f.close()

        # Unlock valt with key
        cipher = AES.new(self.getHash(), AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

        # Set vault content to class level var
        self.vault = json.loads(data.decode("utf-8"))

    def getHash(self):
        """
            Returns a 32 bytes hash for a given master key
        """

        h = SHA256.new()
        for i in range(1, 10000):
            h.update(str.encode(str(i) + self.config['salt'] + self.masterKey))
        return base64.b64decode(str.encode(h.hexdigest()[:32]))

    def addItemInput(self):
        """
            Add a new secret based on user input
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        if self.vault.get('categories'):
            # Show categories
            print()
            print("* Available categories:")
            self.categoriesList()
            print()

            # Category ID
            while True:
                try:
                    categoryId = self.input(
                        '* Choose a category number (or leave empty for none): ')
                    break
                except KeyboardInterrupt as e:
                    # Back to menu if user cancels
                    print()
                    return
                except Exception as e:  # Other Exception
                    print()
                    pass

            if categoryId != '':
                if not self.categoryCheckId(categoryId):
                    print('Invalid category. Please try again.')
                    self.addItemInput()
        else:
            print()
            categoryId = ''
            print("* Category: you did not create a category yet. Create one from the main menu to use this feature!")

        # Basic settings
        try:
            name = self.input('* Name / URL: ')
            login = self.input('* Login: ')
            print('* Password suggestion: %s' % (pwgenerator.generate()))
            password = getpass.getpass('* Password: ')

            # Notes
            print('* Notes: (press [ENTER] twice to complete)')
            notes = []
            while True:
                input_str = self.input("> ")
                if input_str == "":
                    break
                else:
                    notes.append(input_str)
        except KeyboardInterrupt as e:
            return

        # Save item
        self.addItem(categoryId, name, login, password, "\n".join(notes))

        # Confirmation
        print()
        print('The new item has been saved to your vault.')
        print()

    def addItem(self, categoryId, name, login, password, notes):
        """
            Add a new secret to the vault
        """

        # Create `secret` item if necessary
        if not self.vault.get('secrets'):
            self.vault['secrets'] = []

        # Add item to vault
        self.vault['secrets'].append({
            'category': categoryId,
            'name': name,
            'login': login,
            'password': password,
            'notes': notes
        })

        self.saveVault()

    def menu(self):
        """
            Display user menu
        """

        # Initial value
        nextCommand = None

        while (True):
            # Check then set auto lock timer
            self.checkThenSetAutoLockTimer()

            if nextCommand:  # If we already know the next command
                command = nextCommand
                nextCommand = None  # reset
            else:  # otherwise, ask for user input
                print()
                while True:
                    try:
                        command = self.input(
                            'Choose a command [(s)earch / show (all) / (a)dd / (cat)egories / (l)ock / (q)uit]: ', ['l', 'q'])
                        break
                    except KeyboardInterrupt as e:
                        # Back to menu if user cancels
                        print()
                        continue
                    except Exception as e:  # Other Exception
                        print()
                        pass

            # Ensure the input is lowercased
            command = command.lower()

            # Action based on command
            if command == 's':  # Search an item
                nextCommand = self.search()
            elif command == 'all':  # Show all items
                self.all()
            elif command == 'a':  # Add an item
                self.addItemInput()
            elif command == 'cat':  # Manage categories
                self.categoriesMenu()
            elif command == 'l':  # Lock the vault and ask for the master key
                self.lock()
            elif command == 'q':  # Lock the vault and quit
                self.quit()

    def get(self, id):
        """
            Quickly retrieve an item from the vault with its ID
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        try:
            # Get item
            item = self.vault['secrets'][int(id)]

            # Show item in a table
            results = [[
                self.categoryName(item['category']),
                item['name'],
                item['login']
            ]]
            from tabulate import tabulate
            print()
            print(tabulate(results, headers=[
                  'Category', 'Name / URL', 'Login']))

            # Show eventual notes
            if item['notes'] != '':
                print()
                print('Notes:')
                print(item['notes'])

            # Show item menu
            return self.itemMenu(int(id), item)
        except Exception as e:
            print(e)
            print('Item does not exist.')

    def itemMenu(self, itemKey, item):
        """
            Item menu
        """

        while (True):
            # Check then set auto lock timer
            self.checkThenSetAutoLockTimer()

            print()
            while True:
                try:
                    command = self.input(
                        'Choose a command [copy (l)ogin or (p)assword to clipboard / sh(o)w password / (e)dit / (d)elete / (s)earch / (b)ack to Vault]: ')
                    break
                except KeyboardInterrupt as e:
                    # Back to menu if user cancels
                    print()
                    return
                except Exception as e:  # Other Exception
                    print()
                    pass

            # Ensure the input is lowercased
            command = command.lower()

            # Action based on command
            if command == 'l':  # Copy login to the clipboard
                self.itemCopyToClipboard(item['login'], 'login')
            elif command == 'p':  # Copy a secret to the clipboard
                self.itemCopyToClipboard(item['password'])
            elif command == 'o':  # Show a secret
                self.itemShowSecret(item['password'])
            elif command == 'e':  # Edit an item
                self.itemEdit(itemKey, item)
                return
            elif command == 'd':  # Delete an item
                self.itemDelete(itemKey)
                return
            elif command in ['s', 'b', 'q']:  # Common commands
                return command

    def itemCopyToClipboard(self, item, name='password'):
        """
            Copy an item to the clipboard
        """

        # Copy to clipboard
        self.clipboard(item)
        print('* The %s has been copied to the clipboard.' % (name))
        self.waitAndEraseClipboard()

    def itemShowSecret(self, password):
        """
            Show a secret for X seconds and erase it from the screen
        """

        try:
            print("The password will be hidden after %s seconds." %
                  (self.config['hideSecretTTL']))
            print('The password is: %s' % (password), end="\r")

            time.sleep(int(self.config['hideSecretTTL']))
        except KeyboardInterrupt as e:
            # Will catch `^-c` and immediately hide the password
            pass

        print('The password is: ' + '*' * len(password))

    def itemEdit(self, itemKey, item):
        """
            Edit an item
        """

        while (True):
            # Check then set auto lock timer
            self.checkThenSetAutoLockTimer()

            print()
            while True:
                try:
                    command = self.input(
                        'Choose what you would like to edit [(c)ategory / (n)ame / (l)ogin / (p)assword / n(o)tes / (b)ack to Vault]: ')
                    break
                except KeyboardInterrupt as e:
                    # Back to menu if user cancels
                    print()
                    return
                except Exception as e:  # Other Exception
                    print()
                    pass

            # Ensure the input is lowercased
            command = command.lower()

            # Action based on command
            if command == 'c':  # Edit category
                self.editItemInput(itemKey, 'category',
                                   self.categoryName(item['category']))
                return
            elif command == 'n':  # Edit name
                self.editItemInput(itemKey, 'name', item['name'])
                return
            elif command == 'l':  # Edit login
                self.editItemInput(itemKey, 'login', item['login'])
                return
            elif command == 'p':  # Edit password
                self.editItemInput(itemKey, 'password', '')
                return
            elif command == 'o':  # Edit notes
                self.editItemInput(itemKey, 'notes', item['notes'])
                return
            elif command == 'b':  # Back to vault menu
                return

    def editItemInput(self, itemKey, fieldName, fieldCurrentValue):
        """
            Edit a field for an item
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        # Show current value
        if fieldName != 'password':
            print("* Current value: %s" % (fieldCurrentValue))

        try:
            # Get new value
            if fieldName == 'password':
                print('* Suggestion: %s' % (pwgenerator.generate()))
                fieldNewValue = getpass.getpass('* New password: ')
            elif fieldName == 'category':
                # Show categories
                print()
                print("* Available categories:")
                self.categoriesList()
                print()

                # Category ID
                fieldNewValue = self.input(
                    '* Choose a category number (or leave empty for none): ')

                if fieldNewValue != '':
                    if not self.categoryCheckId(fieldNewValue):
                        print('Invalid category. Please try again.')
                        self.editItemInput(
                            itemKey, fieldName, fieldCurrentValue)
            elif fieldName == 'notes':
                print('* Notes: (press [ENTER] twice to complete)')
                notes = []
                while True:
                    input_str = self.input("> ")
                    if input_str == "":
                        break
                    else:
                        notes.append(input_str)
                fieldNewValue = "\n".join(notes)
            else:
                fieldNewValue = self.input('* New %s: ' % (fieldName))
        except KeyboardInterrupt as e:
            # Back to menu if user cancels
            print()
            return

        # Update item
        item = self.vault['secrets'][itemKey][fieldName] = fieldNewValue

        # Debug
        # print(self.vault['secrets'][itemKey])

        # Save the vault
        self.saveVault()

        print('The item has been updated.')

    def itemDelete(self, itemKey):
        """
            Delete an item
        """

        from .Misc import confirm

        try:
            # Get item
            item = self.vault['secrets'][itemKey]

            # Show item
            print()
            if confirm('Confirm deletion?', False):
                # Remove item
                self.vault['secrets'].pop(itemKey)

                # Save the vault
                self.saveVault()
        except Exception as e:
            print('Item does not exist.')

    def search(self):
        """
            Search items
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        print()
        while True:
            try:
                search = self.input('Enter search: ')
                break
            except KeyboardInterrupt as e:
                # Back to menu if user cancels
                print()
                return
            except Exception as e:  # Other Exception
                print()
                pass

        # Return to menu if search is empty
        if search == '':
            # Back to menu if user cancels
            print()
            print('Empty search!')
            return

        # To prevent fat-finger errors, the search menu will also respond to common commands
        if search in ['s', 'a', 'l', 'q']:  # Common commands
            return search
        elif search == 'b':  # Return to previous menu
            return

        if self.vault.get('secrets'):
            # Check if the user inputed an item number
            if search.isdigit():
                # Get item
                try:
                    # Will return an IndexError if the item does not exists
                    self.vault['secrets'][int(search)]
                    return self.get(int(search))
                except IndexError:
                    pass

            # Iterate thru the items
            results = []
            searchResultItems = {}
            searchResultItemNumber = 0
            for i, item in enumerate(self.vault['secrets']):
                # Search in name, login and notes
                if search.upper() in item['name'].upper() or \
                        search.upper() in item['login'].upper() or \
                        search.upper() in item['notes'].upper() or \
                        search.upper() in self.categoryName(item['category']).upper():
                    # Increment search result item number
                    searchResultItemNumber += 1

                    # Set search result value
                    searchResultItems[searchResultItemNumber] = i

                    # Add item to search results
                    results.append([
                        searchResultItemNumber,
                        i,
                        self.categoryName(item['category']),
                        item['name'],
                        item['login']
                    ])

            # If we have search results
            if len(results) == 1:  # Exactly one result
                # Get ID
                id = searchResultItems[1]

                # Load item
                return self.get(id)
            elif len(results) > 1:  # More than one result
                # Show results table
                from tabulate import tabulate
                print()
                print(tabulate(results, headers=[
                      '#', 'Item', 'Category', 'Name / URL', 'Login']))

                return self.searchResultSelection(searchResultItems)
            else:
                print('No results!')
        else:
            print("There are no secrets saved yet.")

    def searchResultSelection(self, searchResultItems):
        """
            Allow the user to select a search result or to go back to the main menu
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        print()
        while True:
            try:
                resultItem = self.input(
                    'Select a result # or type any key to go back to the main menu: ')
                break
            except KeyboardInterrupt as e:
                # Back to menu if user cancels
                print()
                return
            except Exception as e:  # Other Exception
                print()
                pass

        # Try getting an item or send user back to the main menu
        try:
            # Get item ID
            id = searchResultItems[int(resultItem)]

            return self.get(id)
        except Exception as e:
            # Back to menu if user cancels
            print()
            return

    def all(self):
        """
            Show all items in a table
        """

        if self.vault.get('secrets'):
            # Iterate thru the items
            results = []
            for i, item in enumerate(self.vault['secrets']):
                # Add item to results
                results.append([
                    i,
                    self.categoryName(item['category']),
                    item['name'],
                    item['login']
                ])

            # Show results table
            from tabulate import tabulate
            print()
            print(tabulate(results, headers=[
                  'Item', 'Category', 'Name / URL', 'Login']))
        else:
            print("There are no secrets saved yet.")

    def lock(self):
        """
            Lock the vault and ask the user to login again
        """

        # Lock the vault
        self.vault = None

        # Unlock form
        self.unlock(False)

    def quit(self):
        """
            Lock the vault and exit the program
        """

        # Lock the vault
        self.vault = None

        # Exit program
        sys.exit()

    def showSecretCount(self):
        """
            If the vault has secrets, this method will show the total number of secrets.
        """

        if self.vault.get('secrets'):
            count = len(self.vault['secrets'])

            print()
            if count > 1:
                print("%s items are saved in the vault" % (count))
            else:
                print("%s item is saved in the vault" % (count))

    def categoriesMenu(self):
        """
            Categories menu
        """

        while (True):
            # Check then set auto lock timer
            self.checkThenSetAutoLockTimer()

            # List categories
            self.categoriesList()

            print()
            while True:
                try:
                    command = self.input(
                        'Choose a command [(a)dd a category / (r)rename a category / (d)elete a category / (b)ack to Vault]: ')
                    break
                except KeyboardInterrupt as e:
                    # Back to menu if user cancels
                    print()
                    return
                except Exception as e:  # Other Exception
                    print()
                    pass

            # Ensure the input is lowercased
            command = command.lower()

            # Action based on command
            if command == 'a':  # Add a category
                self.categoryAdd()
                return
            elif command == 'r':  # Rename a category
                self.categoryRename()
                return
            elif command == 'd':  # Delete a category
                self.categoryDelete()
                return
            elif command == 'b':  # Back to vault menu
                return

    def categoriesList(self):
        """
            List all categories
        """

        if self.vault.get('categories'):
            # Iterate thru the items
            results = []
            for i, item in enumerate(self.vault['categories']):
                # Add item to results
                if item['active'] is True:
                    results.append([
                        i,
                        item['name']
                    ])

            # If we have active categories
            if len(results) > 0:
                # Show results table
                from tabulate import tabulate
                print()
                print(tabulate(results, headers=['Item', 'Category name']))
            else:
                print('There are no categories yet.')
        else:
            print()
            print("There are no categories yet.")

    def categoryAdd(self):
        """
            Create a new category
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        # Basic input
        try:
            name = self.input('Category name: ')
        except KeyboardInterrupt as e:
            # Back to menu if user cancels
            print()
            return

        # Create `categories` item if necessary
        if not self.vault.get('categories'):
            self.vault['categories'] = []

        # Add new category to vault
        self.vault['categories'].append({
            'name': name,
            'active': True
        })

        self.saveVault()

        # Confirmation
        print()
        print('The category has been created.')

    def categoryDelete(self):
        """
            Quickly delete a category from the vault with its ID
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        from .Misc import confirm

        print()
        try:
            id = self.input('Enter category number: ')
        except KeyboardInterrupt as e:
            # Back to menu if user cancels
            print()
            return

        try:
            # Get item
            item = self.vault['categories'][int(id)]

            # Show item
            print('* Category: %s' % (item['name']))
            print()
            if self.categoryIsUsed(id) is False:
                if confirm('Confirm deletion?', False):
                    if self.categoryIsUsed(id) is False:
                        # Deactivate item
                        self.vault['categories'][int(id)]['active'] = False

                        # Save the vault
                        self.saveVault()

                        print('The category has been deleted.')
            else:
                print(
                    'The category cannot be deleted because it is currently used by some secrets.')
        except Exception as e:
            print('Category does not exist.')

    def categoryIsUsed(self, categoryId):
        """
            Will return `True` if a category is currently used by a secret
        """

        if self.vault.get('secrets'):
            # Iterate thru the items
            for item in self.vault['secrets']:
                # If the item has a category and it is the category searched
                if categoryId and item['category'] == categoryId:
                    return True
        else:
            return False

        return False

    def categoryRename(self):
        """
            Quickly rename a category from the vault with its ID
        """

        # Set auto lock timer (to prevent immediate re-locking)
        self.setAutoLockTimer()

        from .Misc import confirm

        print()
        try:
            id = self.input('Enter category number: ')
        except KeyboardInterrupt as e:
            # Back to menu if user cancels
            print()
            return

        try:
            # Get item
            item = self.vault['categories'][int(id)]

            # Show item
            print('* Category: %s' % (item['name']))

            # Basic input
            name = input('* New category name: ')

            # Deactivate item
            self.vault['categories'][int(id)]['name'] = name

            # Save the vault
            self.saveVault()

            print('The category has been renamed.')
        except Exception as e:
            print('Category does not exist.')

    def categoryCheckId(self, categoryId):
        """
            When adding a secret, check if a category ID is valid
        """

        try:
            # Get item
            item = self.vault['categories'][int(categoryId)]

            if item['active'] is True:  # Return `true` if the category is active
                return True
        except Exception as e:
            return False

        # Default
        return False

    def categoryName(self, categoryId):
        """
            Returns a category name
        """

        try:
            # Get item
            item = self.vault['categories'][int(categoryId)]

            if item['active'] is True:  # Return category name if the category is active
                return item['name']
        except Exception as e:
            return 'n/a'

        # Default
        return 'n/a'

    def clipboard(self, toCopy):
        """
            Copy an item to the clipboard
        """

        pyperclip.copy(toCopy)

        # Save signature
        self.clipboardSignature = self.getSignature(toCopy)

    def isClipboardChanged(self):
        """
            Returns `True` if the clipboard content has changed
        """

        return self.clipboardSignature != self.getSignature(pyperclip.paste())

    def getSignature(self, item):
        """
            Returns the sha256 hash of a string
        """

        h = SHA256.new()
        h.update(str.encode(item))
        return h.hexdigest()

    def waitAndEraseClipboard(self):
        """
            Wait X seconds and erase the clipboard
        """

        print("* Clipboard will be erased in %s seconds" %
              (self.config['clipboardTTL']))

        try:
            # Loop until the delay is elapsed
            for i in range(0, int(self.config['clipboardTTL'])):
                print('.', end='', flush=True)
                time.sleep(1)  # Sleep 1 sec

                # Stop timer if clipboard content has changed
                if self.isClipboardChanged():
                    break
        except KeyboardInterrupt as e:
            # Will catch `^-c` and immediately erase the clipboard
            pass

        print()
        if not self.isClipboardChanged():  # We will not empty the clipboard if its content has changed
            self.clipboard('')  # Empty clipboard
        self.clipboardSignature = ''  # Reset clipboard signature

    def changeKey(self):
        """
            Replace vault key
            Will ask user to initially unlock the vault
            Then the user will input a new master key and the vault will be saved with the new key
        """

        # Unlock the vault with the existing key
        if self.vault is None:  # Except if the vault already unlocked
            self.unlock(False)  # `False` = don't load menu after unlocking

        # Choose a new key
        print()
        newMasterKey = getpass.getpass(
            self.lockPrefix() + 'Please choose a new master key:')
        newMasterKeyRepeat = getpass.getpass(
            self.lockPrefix() + 'Please confirm your new master key:')

        if len(newMasterKey) < 8:
            print()
            print('The master key should be at least 8 characters. Please try again!')
            print()
            # Try again
            self.changeKey()
        elif newMasterKey == newMasterKeyRepeat:
            # Override master key
            self.masterKey = newMasterKey

            # Save vault with new master key
            self.saveVault()

            print()
            print("Your master key has been updated.")
            self.unlock(False)
        else:
            print()
            print('The master key does not match its confirmation. Please try again!')
            print()
            # Try again
            self.changeKey()

    def getVault(self):
        """
            Returns the vault content
        """

        return self.vault

    def isUnicodeSupported(self):
        """
            Returns `True` if stdout supports unicode
        """
        if sys.stdout.encoding:
            return sys.stdout.encoding.lower().startswith('utf-')

        return False

    def lockPrefix(self):
        """
            Will prefix locks with a Unicode Character 'KEY' (U+1F511)
            if the user's stdout supports it
        """

        if self.isUnicodeSupported():
            return u'\U0001F511  '  # Extra spaces are intentional

        return ''
