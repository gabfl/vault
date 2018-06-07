
class Vault:

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
