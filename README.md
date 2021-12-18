# Vault

[![Pypi](https://img.shields.io/pypi/v/pyvault.svg)](https://pypi.org/project/pyvault)
[![Build Status](https://github.com/gabfl/vault/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/gabfl/vault/actions)
[![codecov](https://codecov.io/gh/gabfl/vault/branch/main/graph/badge.svg)](https://codecov.io/gh/gabfl/vault)
[![MIT licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://raw.githubusercontent.com/gabfl/vault/main/LICENSE)

Vault is a simple Python password manager. It allows you to securely save secrets with a simple CLI interface.

## Features

 - Secrets are stored in an encrypted SQLite database with [SQLCipher](https://www.zetetic.net/sqlcipher/)
 - Within the database, each password and notes are encrypted with a unique salt using AES-256 encryption with [pycryptodome](http://legrandin.github.io/pycryptodome/)
 - Master key is hashed with a unique salt
 - Possibility to create an unlimited number of vaults
 - Clipboard cleared automatically
 - Automatic vault locking after inactivity
 - Password suggestions with [password-generator-py](https://github.com/gabfl/password-generator-py)
 - Import / Export in Json

## Basic usage

![Demo](https://github.com/gabfl/vault/blob/main/img/demo.gif?raw=true)

## Installation and setup

### Install sqlcipher

Vault 2.x requires `sqlcipher` to be installed on your machine.

On MacOS, you can install it with [brew](https://brew.sh/):
```bash
brew install sqlcipher

# Install sqlcipher3
pip3 install sqlcipher3==0.4.5

# If you are getting an error "Failed to build sqlcipher3", you would need to fix the build flags:
SQLCIPHER_PATH="$(brew --cellar sqlcipher)/$(brew list --versions sqlcipher | tr ' ' '\n' | tail -1)"
C_INCLUDE_PATH=$SQLCIPHER_PATH/include LIBRARY_PATH=$SQLCIPHER_PATH/lib pip3 install sqlcipher3==0.4.5
```

On Ubuntu/Debian, you can install it with apt-get:
```bash
sudo apt-get update
sudo apt-get install --yes gcc python3-dev libsqlcipher-dev
```

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
             [-k] [-i IMPORT_ITEMS] [-x EXPORT] [-f [{json}]] [-e]

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
  -f [{json}], --file_format [{json}]
                        Import/export file format (default: 'json')
  -e, --erase_vault     Erase the vault and config file
```
