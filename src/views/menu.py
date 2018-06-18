import sys
import time
import getpass

from ..modules.carry import global_scope
from ..models.base import get_engine, get_session
from ..modules.misc import lock_prefix, clear_screen, logo_small
from ..lib.Encryption import Encryption
from . import secrets, users, categories

timer = None


def get_input(message='', secure=False, lowercase=False, check_timer=True, non_locking_values=[]):
    """
        Get and return user input
    """

    try:
        if secure:
            input_ = getpass.getpass(lock_prefix() + message)
        else:
            input_ = input(message)

        if check_timer and input_ not in non_locking_values:
            check_then_set_autolock_timer()
        else:
            set_autolock_timer()

        # Ensure the input is lowercased if required
        if lowercase:
            input_ = input_.lower()
    except KeyboardInterrupt:
        return False
    except Exception:  # Other Exception
        return False

    return input_


def unlock(redirect_to_menu=True, tentative=1):
    """
        Asking the user for his master key and trying to unlock the vault
    """

    # Get master key
    print()
    key = get_input(message='Please enter your master key:',
                    secure=True, check_timer=False)

    # Exit if the user pressed Ctrl-C
    if key is False:
        print()
        sys.exit()

    if validate_key(key):
        if redirect_to_menu:
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
    return users.validation_key_validate(key.encode())


def menu(next_command=None):
    """
        Display user menu
    """

    while (True):
        # Check then set auto lock timer
        check_then_set_autolock_timer()

        # Clear screen
        clear_screen()

        # Small logo
        logo_small()

        # Secret count
        print("\n%s items are saved in the vault" % (secrets.count()))

        if next_command:  # If we already know the next command
            command = next_command
            next_command = None  # reset
        else:  # otherwise, ask for user input
            print()
            command = get_input(
                message='Choose a command [(s)earch / show (all) / (a)dd / (cat)egories / (l)ock / (q)uit]: ',
                lowercase=True,
                non_locking_values=['l', 'q'])

            if command is False:
                print()

        # Action based on command
        if command == 's':  # Search an item
            next_command = secrets.search_input()
        elif command == 'all':  # Show all items
            print()
            print(secrets.to_table(secrets.all()))
            next_command = secrets.search_input()
        elif command == 'a':  # Add an item
            secrets.add_input()
        elif command == 'cat':  # Manage categories
            categories.main_menu()
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

    # Clear screen
    clear_screen()

    # Small logo
    logo_small()

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

    if timer and int(time.time()) > timer + int(global_scope['conf'].autoLockTTL):
        print()
        print("The vault has been locked due to inactivity.")
        lock()


def check_then_set_autolock_timer():
    """
        Check auto lock timer and lock the vault if necessary, then set it again
    """

    check_autolock_timer()
    set_autolock_timer()
