import os
import sys

import argparse

from .lib.Config import Config
from .modules.misc import logo, create_directory_if_missing, assess_integrity, erase_vault
from .views import setup, change_key
from .views.menu import unlock
from .views.import_export import import_, export_
from .views.migration import migrate
from .modules.carry import global_scope

# Default paths
dir_ = os.path.expanduser('~') + '/.vault/'
config_path_default = dir_ + '.config'
vault_path_default = dir_ + '.secure.db'


def get_vault_path(override=None):
    """
        Returns the vault location (either default or user defined)
    """

    global vault_path_default

    if override:
        return override
    return vault_path_default


def get_config_path(override=None):
    """
        Returns the config location (either default or user defined)
    """

    global config_path_default

    if override:
        return override
    return config_path_default


def check_directory(vault_path, config_path):
    """
        Create the vault folder if it does not exists yet
    """

    if vault_path == vault_path_default or config_path == config_path_default:
        return create_directory_if_missing(dir_)

    return None


def config_update(clipboard_TTL=None, auto_lock_TTL=None, hide_secret_TTL=None):
    """
        Update config
    """

    if clipboard_TTL:
        return global_scope['conf'].update('clipboardTTL', clipboard_TTL)
    elif auto_lock_TTL:
        return global_scope['conf'].update('autoLockTTL', auto_lock_TTL)
    elif hide_secret_TTL:
        return global_scope['conf'].update('hideSecretTTL', hide_secret_TTL)


def initialize(vault_location_override, config_location_override, erase=None, clipboard_TTL=None, auto_lock_TTL=None, hide_secret_TTL=None, rekey_vault=None, import_items=None, export=None, file_format='json'):
    # Some nice ascii art
    logo()

    # Set vault and config path
    vault_path = get_vault_path(vault_location_override)
    config_path = get_config_path(config_location_override)

    # Set vault path at the global scope
    global_scope['db_file'] = vault_path

    # Create the vault folder if it does not exists yet
    check_directory(vault_path, config_path)

    # Assess files integrity
    assess_integrity(vault_path, config_path)

    # Erase a vault if the user requests it
    if erase:
        erase_vault(vault_path, config_path)
        sys.exit()

    # Load config
    global_scope['conf'] = Config(config_path)

    # Migration from Vault 1.x to Vault 2.x
    if global_scope['conf'].version.split('.')[0] == '1':
        migrate(vault_path=vault_path.strip('.db'), config_path=config_path)
        sys.exit()

    # Update config
    config_update(clipboard_TTL, auto_lock_TTL, hide_secret_TTL)

    # Change vault key
    if rekey_vault:
        print()
        # print("Please consider backing up your vault located at `%s` before proceeding." % (
        #     vault_path))
        # change_key.rekey()
        print('This feature is not currently implemented.')
        print('Please export the vault to a Json file, create a new vault with the new key and import the Json file in the new vault.')
        sys.exit()

    # Import items in the vault
    if import_items:
        print()
        print("Please consider backing up your vault located at `%s` before proceeding." % (
            vault_path))
        import_(format_=file_format, path=import_items)
        sys.exit()

    # Export vault
    if export:
        export_(format_=file_format, path=export)
        sys.exit()

    # Check if the vault exists
    if not os.path.isfile(vault_path):
        res = setup.initialize(global_scope['conf'].salt)
        if res is False:
            print()
            return False

    # Unlock the vault
    unlock()


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--clipboard_TTL", type=int,
                        help="Set clipboard TTL (in seconds, default: 15)", nargs='?', const=15)
    parser.add_argument("-p", "--hide_secret_TTL", type=int,
                        help="Set delay before hiding a printed password (in seconds, default: 15)", nargs='?', const=5)
    parser.add_argument("-a", "--auto_lock_TTL", type=int,
                        help="Set auto lock TTL (in seconds, default: 900)", nargs='?', const=900)
    parser.add_argument("-v", "--vault_location",
                        type=str, help="Set vault path")
    parser.add_argument("-c", "--config_location",
                        type=str, help="Set config path")
    parser.add_argument("-k", "--change_key",
                        action='store_true', help="Change master key")
    parser.add_argument("-i", "--import_items", type=str,
                        help="File to import credentials from")
    parser.add_argument("-x", "--export", type=str,
                        help="File to export credentials to")
    parser.add_argument("-f", "--file_format", type=str, help="Import/export file format (default: 'json')",
                        choices=['json'], nargs='?', default='json')
    parser.add_argument("-e", "--erase_vault", action='store_true',
                        help="Erase the vault and config file")
    args = parser.parse_args()

    initialize(vault_location_override=args.vault_location,
               config_location_override=args.config_location,
               erase=args.erase_vault,
               clipboard_TTL=args.clipboard_TTL,
               auto_lock_TTL=args.auto_lock_TTL,
               hide_secret_TTL=args.hide_secret_TTL,
               rekey_vault=args.change_key,
               import_items=args.import_items,
               export=args.export,
               file_format=args.file_format)


if __name__ == '__main__':
    main()
