# Vault

Vault is a simple Python password manager. It allows you to securely save secrets with a simple CLI interface.

## Features

 - AES-256 encryption with [pycryptodome](http://legrandin.github.io/pycryptodome/)
 - Secret key is hashed with a unique salt (100,000 iterations)
 - Possibility to create an unlimited number of vaults
 - Clipboard cleared automatically
 - Automatic vault locking after inactivity
 - Import / Export in Json

## Install dependencies

```
pip3 install pycryptodome pyperclip tabulate argparse
```

## Installation and setup

```
# Clone project
git clone https://github.com/gabfl/vault
cd vault

# Run setup
python3 vault.py
```

### Basic usage:
```
./vault.py
    __      __         _ _           .----.
    \ \    / /        | | |         / /  \ \
     \ \  / /_ _ _   _| | |_       _| |__| |_
      \ \/ / _` | | | | | __|    .' |_   |_| '.
       \  / (_| | |_| | | |_     '.__________.'
        \/ \__,_|\__,_|_|\__|    |            |
                                 '.__________.'
Please enter your master key:

Choose a command [(g)et / (s)earch / show (all) / (a)dd / (d)elete / (cat)egories / (l)ock / (q)uit]:
```

### Advanced settings:

```
usage: vault.py [-h] [-t [CLIPBOARD_TTL]] [-a [AUTO_LOCK_TTL]]
                [-v VAULT_LOCATION] [-c CONFIG_LOCATION] [-k]
                [-i IMPORT_ITEMS] [-x EXPORT] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -t [CLIPBOARD_TTL], --clipboard_TTL [CLIPBOARD_TTL]
                        Set clipboard TTL (in seconds, default: 15)
  -a [AUTO_LOCK_TTL], --auto_lock_TTL [AUTO_LOCK_TTL]
                        Set auto lock TTL (in seconds, default: 900)
  -v VAULT_LOCATION, --vault_location VAULT_LOCATION
                        Set vault path
  -c CONFIG_LOCATION, --config_location CONFIG_LOCATION
                        Set config path
  -k, --change_key      Change master key
  -i IMPORT_ITEMS, --import_items IMPORT_ITEMS
                        File to import credentials from
  -x EXPORT, --export EXPORT
                        File to export credentials to
  -e, --erase_vault     Erase the vault and config file
```
