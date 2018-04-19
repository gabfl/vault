
def logo():
    """
        No comment.
    """

    print(r"    __      __         _ _           .----.    ")
    print(r"    \ \    / /        | | |         / /  \ \   ")
    print(r"     \ \  / /_ _ _   _| | |_       _| |__| |_  ")
    print(r"      \ \/ / _` | | | | | __|    .' |_   |_| '.")
    print(r"       \  / (_| | |_| | | |_     '.__________.'")
    print(r"        \/ \__,_|\__,_|_|\__|    |            |")
    print(r"                                 '.__________.'")


def createFolderIfMissing(folderPath):
    """
        Create the vault and configuration file storage folder if it does not exist
    """

    import os

    try:
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
    except Exception as e:
        import sys

        print()
        print('We were unable to create the folder `%s` to store the vault and configuration file.' % (
            folderPath))
        print('Please check the permissions or run `./vault.py --help` to find out how to specify an alternative path for both files.')
        print()
        sys.exit()


def assessIntegrity(vaultPath, configPath):
    """
        The vault config file contains a salt. The salt is used to unlock the vault along with the master key.
        By default, config files are created automatically. A new config file will not allow to open an existing vault.
        We are ensuring here that a config file exists if a vault exists.
    """

    import os
    import sys

    if not os.path.isfile(configPath) and os.path.isfile(vaultPath):
        print()
        print("It looks like you have a vault setup but your config file is missing.")
        print("The vault cannot be unlocked without a critical piece of information from the config file (the salt).")
        print("Please restore the config file before proceeding.")
        print()
        sys.exit()


def eraseVault(vaultPath, configPath):
    """
        Will erase the vault and config file after asking user for confirmation
    """

    import os
    import sys

    print()
    if confirm(prompt='Do you want to permanently erase your vault? All your data will be lost!', resp=False):
        # Delte files
        if os.path.isfile(vaultPath):
            os.remove(vaultPath)
        if os.path.isfile(configPath):
            os.remove(configPath)

        print()
        print('The vault and config file have been deleted.')
        print()
        sys.exit()
    else:
        sys.exit()


def confirm(prompt=None, resp=False):
    """
        Source: http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/

        prompts for yes or no response from the user. Returns True for yes and
        False for no.

        'resp' should be set to the default value assumed by the caller when
        user simply types ENTER.

        >>> confirm(prompt='Create Directory?', resp=True)
        Create Directory? [y]|n:
        True
    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [Y/n]: ' % (prompt)
    else:
        prompt = '%s [y/N]: ' % (prompt)

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False
