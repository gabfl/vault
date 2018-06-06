
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

from ..modules.misc import confirm, lock_prefix


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
            lock_prefix() + 'Please choose a new master key:')
        newMasterKeyRepeat = getpass.getpass(
            lock_prefix() + 'Please confirm your new master key:')

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
