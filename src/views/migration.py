# Migration helper from Vault 1.x to Vault 2.x
# This tool will read a vault content generated under the legacy format
# and create an import dict compatible with import_export.import_()

import json
import base64
import sys

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from ..modules.carry import global_scope
from ..lib.Config import Config
from ..lib.Encryption import Encryption
from .setup import create_db
from .users import validation_key_new
from .import_export import import_from_json
from . import menu

config = None


def migrate(vault_path, config_path, new_vault_path=None):
    """
        Migrate Vault 1.x to 2.x
    """

    global config

    # Set new vault path
    if new_vault_path is None:
        new_vault_path = vault_path + '.db'

    print()
    print('*' * 23)
    print('* Welcome to Vault 2 *')
    print('*   Migration tool   *')
    print('*' * 23)
    print()
    print('Welcome to Vault 2!')
    print('In Vault 2, all your secrets are stored in a SQLite database.')
    print('The content of your vault needs to be migrated to the new format.')
    print('Just type your master key and folllow the instructions!')
    print()

    # Load config
    config = Config(config_path)

    # Ask user to input master key
    key = menu.get_input(
        message=' * Enter your master key to begin the migration: ', secure=True, check_timer=False)

    # Unlock the vault
    try:
        vault = unlock(vault_path, key)
    except Exception:
        print('Invalid password.')
        print()
        sys.exit()

    # Prepare items for import
    import_ = prepare_items(vault['secrets'], vault['categories'])

    # Create Encryption instance and set it to the global scope
    global_scope['enc'] = Encryption(key.encode())

    # Set db file
    global_scope['db_file'] = new_vault_path

    # Create db
    create_db()

    # Create validation key
    validation_key_new()

    # Import items in the new db
    result = import_from_json(rows=import_)
    if result is False:
        return False

    # Update config
    update_config()

    print()
    print('The migration is now complete!')
    print('Restart the application to use Vault 2.')
    print('Your old vault is stored in `%s`. You can discard this file after ensuring that all your data was migrated properly.' % (vault_path))
    print('Your new vault is stored in `%s`.' % (new_vault_path))
    print()

    return True


def update_config():
    """
        Update flags in config file
    """

    config.update('version', '2.00')
    config.update('encrypteddb', True)


def unlock(vault_path, key):
    """
        Unlock legacy vault and retrieve content
    """

    f = open(vault_path, "rb")
    try:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
    finally:
        f.close()

    # Unlock Vault with key
    cipher = AES.new(get_hash(key), AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # Set vault content to class level var
    return json.loads(data.decode("utf-8"))


def get_hash(key):
    """
        Returns a 32 bytes hash for a given master key
    """

    h = SHA256.new()
    for i in range(1, 10000):
        h.update(str.encode(
            str(i) + config.salt + key))
    return base64.b64decode(str.encode(h.hexdigest()[:32]))


def prepare_items(secrets, categories):
    """
        Prepare all secrets to the new import format
    """

    out = []
    for secret in secrets:
        out.append({
            'name': secret.get('name'),
            'url': None,  # Not supported in legacy database
            'login': secret.get('login'),
            'password': secret.get('password'),
            'notes': secret.get('notes'),
            'category': get_category_name(secret.get('category'), categories),
        })

    return out


def get_category_name(id_, categories):
    """
        Return category name
    """

    if id_ is None or id_ == '':
        return None

    item = categories[int(id_)]
    if item['active'] is True:
        return item['name']

    return None
