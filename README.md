# Vault

Vault is a simple Python password manager. It allows you to securely save secrets with a simple CLI interface.

## Features

 - AES-256 encryption with [pycryptodome](http://legrandin.github.io/pycryptodome/)
 - Secret key is hashed with a unique salt (100,000 iterations)
 - Possibility to create an unlimited number of vaults
 - Clipboard cleared automatically
 - Automatic vault locking after inactivity
 - Password suggestions with [password-generator-py](https://github.com/gabfl/password-generator-py)
 - Import / Export in Json

## Basic usage

![Demo](https://github.com/gabfl/vault/blob/master/img/demo.gif?raw=true)

## Installation and setup

### Using PyPI

```bash
pip3 install pyvault

# Run setup
vault
```

### Cloning the project

```bash
# Clone project
git clone https://github.com/gabfl/vault && cd vault

# Installation
python3 setup.py install

# Run setup
vault
```

## Advanced settings:

```
usage: vault [-h] [-t [CLIPBOARD_TTL]] [-p [HIDE_SECRET_TTL]]
             [-a [AUTO_LOCK_TTL]] [-v VAULT_LOCATION] [-c CONFIG_LOCATION]
             [-k] [-i IMPORT_ITEMS] [-x EXPORT] [-f [{json,native}]] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -t [CLIPBOARD_TTL], --clipboard_TTL [CLIPBOARD_TTL]
                        Set clipboard TTL (in seconds, default: 15)
  -p [HIDE_SECRET_TTL], --hide_secret_TTL [HIDE_SECRET_TTL]
                        Set delay before hiding a printed password (in
                        seconds, default: 15)
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
  -f [{json,native}], --file_format [{json,native}]
                        Import/export file format (default: 'json')
  -e, --erase_vault     Erase the vault and config file
```
