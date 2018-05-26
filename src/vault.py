import os

import argparse

from .lib.Vault import Vault
from .lib.Config import Config
from .lib.ImportExport import ImportExport
from .lib.Misc import *

# Default paths
folderPath = os.path.expanduser('~') + '/.vault/'
ConfigPathDefault = folderPath + '.config'
vaultPathDefault = folderPath + '.secure'


def getVaultPath(override=None):
    """
        Returns the vault location (either default or user defined)
    """

    global vaultPathDefault

    if override:
        return override
    return vaultPathDefault


def getConfigPath(override=None):
    """
        Returns the config location (either default or user defined)
    """

    global ConfigPathDefault

    if override:
        return override
    return ConfigPathDefault


def initialize(vault_location, config_location, erase_vault=None, clipboard_TTL=None, auto_lock_TTL=None, hide_secret_TTL=None, change_key=None, import_items=None, export=None, file_format='json'):
    # Some nice ascii art
    logo()

    # Create the vault folder if it does not exists yet
    if getVaultPath(vault_location) == vaultPathDefault or getConfigPath(config_location) == ConfigPathDefault:
        createFolderIfMissing(folderPath)

    # Assess files integrity
    assessIntegrity(getVaultPath(vault_location),
                    getConfigPath(config_location))

    # Erase a vault if the user requests it
    if erase_vault:
        eraseVault(getVaultPath(vault_location),
                   getConfigPath(config_location))

    # Load config
    c = Config(getConfigPath(config_location))
    config = c.getConfig()

    # Update config
    if clipboard_TTL:
        c.update('clipboardTTL', clipboard_TTL)
    elif auto_lock_TTL:
        c.update('autoLockTTL', auto_lock_TTL)
    elif hide_secret_TTL:
        c.update('hideSecretTTL', hide_secret_TTL)

    # Init Vault
    v = Vault(config, getVaultPath(vault_location))

    # Change vault key
    if change_key:
        v.changeKey()

    # Import items to the vault
    if import_items:
        print()
        print("Please consider backing up your vault located at `%s` before proceeding." % (
            getVaultPath(vault_location)))
        ie = ImportExport(v, import_items, file_format)
        ie.importItems()

    # Export vault
    if export:
        ie = ImportExport(v, export, file_format)
        ie.export()

    # Check if the vault exists
    if not os.path.isfile(getVaultPath(vault_location)):
        v.setup()
    # Offer to unlock the vault
    else:
        v.unlock()


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
                        choices=['json', 'native'], nargs='?', default='json')
    parser.add_argument("-e", "--erase_vault", action='store_true',
                        help="Erase the vault and config file")
    args = parser.parse_args()

    initialize(vault_location=args.vault_location,
               config_location=args.config_location,
               erase_vault=args.erase_vault,
               clipboard_TTL=args.clipboard_TTL,
               auto_lock_TTL=args.auto_lock_TTL,
               hide_secret_TTL=args.hide_secret_TTL,
               change_key=args.change_key,
               import_items=args.import_items,
               export=args.export,
               file_format=args.file_format)


if __name__ == '__main__':
    main()
