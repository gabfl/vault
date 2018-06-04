import sys
import time

from ..modules.misc import get_input
from ..modules.carry import global_scope
from ..models.base import get_engine, get_session
from ..lib.Encryption import Encryption
from ..views import secrets, users, categories

timer = None


def get_input_with_autolock(message='', secure=False, lowercase=False, non_locking_values=[]):
    """
        Wrapper arrund get_input() to check autolock timer
    """

    input_ = get_input(message=message,
                       secure=secure,
                       lowercase=lowercase)

    if input_ not in non_locking_values:
        check_autolock_timer()

    return input_


def unlock(redirect_to_menu=True, tentative=1):
    """
        Asking the user for his master key and trying to unlock the vault
    """

    # Get master key
    key = get_input(message='Please enter your master key:', secure=True)

    if validate_key(key):
        if redirect_to_menu:
            print()
            print("%s items are saved in the vault" % (secrets.count()))
            menu()
        else:
            return True
    else:
        if tentative >= 3:
            # Stop trying after 3 attempts
            print('Vault cannot be opened.')
            print()
            sys.exit()
        else:
            # Try again
            print('Master key is incorrect. Please try again!')
            unlock(redirect_to_menu=redirect_to_menu, tentative=tentative + 1)


def validate_key(key):
    """
        Validate a vault key
    """

    # Create instance of Encryption class with the given key
    global_scope['enc'] = Encryption(key.encode())

    # Attempt to unlock the database
    return users.validate_validation_key(key.encode())


def menu(next_command=None):
    """
        Display user menu
    """

    while (True):
        # Check then set auto lock timer
        check_then_set_autolock_timer()

        if next_command:  # If we already know the next command
            command = next_command
            next_command = None  # reset
        else:  # otherwise, ask for user input
            print()
            command = get_input_with_autolock(
                message='Choose a command [(s)earch / show (all) / (a)dd / (cat)egories / (l)ock / (q)uit]: ',
                lowercase=True,
                non_locking_values=['l', 'q'])

        # Action based on command
        if command == 's':  # Search an item
            next_command = self.search()
        elif command == 'all':  # Show all items
            print(secrets.all_table())
        elif command == 'a':  # Add an item
            self.addItemInput()
        elif command == 'cat':  # Manage categories
            categories_menu()
        elif command == 'l':  # Lock the vault and ask for the master key
            lock()
        elif command == 'q':  # Lock the vault and quit
            quit()


def lock():
    """
        Lock the vault and ask the user to login again
    """

    # Lock the vault
    global_scope['enc'] = None

    # Unlock form
    unlock(False)


def quit():
    """
        Exit the program
    """

    # Exit program
    sys.exit()


def set_autolock_timer():
    """
        Set auto lock timer
    """

    global timer

    timer = int(time.time())


def check_autolock_timer():
    """
        Check auto lock timer and lock the vault if necessary
    """

    global timer

    if timer and int(time.time()) > timer + int(global_scope['conf'].getConfig()['autoLockTTL']):
        print()
        print("The vault has been locked due to inactivity.")
        lock()


def check_then_set_autolock_timer():
    """
        Check auto lock timer and lock the vault if necessary, then set it again
    """

    check_autolock_timer()
    set_autolock_timer()


def categories_menu():
    """
        Categories menu
    """

    while (True):
        # Check then set auto lock timer
        check_then_set_autolock_timer()

        # List categories
        print(categories.all_table())

        print()
        command = get_input_with_autolock(
            message='Choose a command [(a)dd a category / (r)rename a category / (d)elete a category / (b)ack to Vault]: ',
            lowercase=True,
            non_locking_values=['l', 'q'])

        # Action based on command
        if command == 'a':  # Add a category
            categories.add_input()
            return
        elif command == 'r':  # Rename a category
            categories.rename_input()
            return
        elif command == 'd':  # Delete a category
            categories.delete_input()
            return
        elif command == 'b':  # Back to vault menu
            return
