"""
    sqlcipher troubleshooting tool
    Usage: python3 -m src.tools.troubleshoot_db
"""

from tempfile import NamedTemporaryFile
import uuid

import sqlcipher3
from sqlalchemy import exc, create_engine

from ..models.base import get_session, drop_sessions, get_db_key
from ..views.menu import get_input
from ..modules.carry import global_scope
from ..lib.Encryption import Encryption
from ..lib.Config import Config
from ..vault import get_config_path, get_vault_path


def load_config():
    """ Load config file """
    config_path = get_config_path()
    global_scope['conf'] = Config(config_path)


def set_vault_path():
    """ Load vault path """
    vault_path = get_vault_path()
    global_scope['db_file'] = vault_path


def get_key_input():
    """ Ask user to input their private key """
    return get_input(message='Please enter your master key:',
                     secure=True, check_timer=False)


def set_encryption(key):
    """ Create instance of Encryption class """
    global_scope['enc'] = Encryption(key.encode())


def get_pragma_key():
    """ Print PRAGMA key used to encrypt db """
    return get_db_key()


def query_vault_db():
    """ Attempt a query against the database """
    try:
        get_session(True).execute('SELECT * FROM sqlite_master')
        return True
    except exc.DatabaseError as e:
        # print('Database Error: %s' % e)
        # print('Most likely, this error is due to an invalid database key or a mis-configured sqlcipher3/libsqlcipher')
        return False


def create_temporary_file():
    """ Create a temporary file to test a dummy encrypted database """
    f = NamedTemporaryFile(delete=False)
    return f.name


def create_temporary_secret():
    """ Create a temporary secret """
    return uuid.uuid4().hex


def attempt_dummy_encrypted_db(db_path):
    """ Create a dummy encrypted database """

    engine = create_engine(
        'sqlite+pysqlcipher://:' + create_temporary_secret() + '@//' + db_path,
        module=sqlcipher3)
    # engine = create_engine('sqlite:///' + db_path)
    connection = engine.connect()
    connection.execute('CREATE TABLE foo (a int)')
    connection.execute('INSERT INTO foo (a) VALUES (123)')
    result_proxy = connection.execute('SELECT * FROM foo')
    return True if result_proxy.fetchall() == [(123,)] else False


def verify_if_dummy_db_is_encrypted(db_path):
    """ Verify if dummy database is correctly encrypted """

    engine = create_engine('sqlite:///' + db_path)
    connection = engine.connect()
    try:
        connection.execute('SELECT * FROM sqlite_master')

        # If query is successful, then the database is not encrypted
        return False
    except exc.DatabaseError as e:
        # sqlite3.DatabaseError: file is not a database
        # print(str(e))
        return True


if __name__ == '__main__':
    temp_db_file = create_temporary_file()
    if attempt_dummy_encrypted_db(temp_db_file):
        print('* Create dummy database: OK')
    else:
        print(
            '!!! Create dummy database: ERROR (Dummy encrypted database could not be created)')

    if verify_if_dummy_db_is_encrypted(temp_db_file):
        print('* Check if dummy database is encrypted: OK')
    else:
        print('!!! Check if dummy database is encrypted: ERROR (Dummy database is not encrypted)')

    load_config()
    set_vault_path()
    key = get_key_input()
    if key:
        set_encryption(key)
        print('* Key is: %s' % global_scope['enc'].key.decode('utf-8'))

        pragma = get_pragma_key()
        print('* Database PRAGMA KEY:')
        print("  sqlcipher %s" % global_scope['db_file'])
        print("  PRAGMA key = '%s';" % pragma)

        if query_vault_db():
            print('* Attempt to query vault: OK')
        else:
            print(
                '!!! Attempt to query vault: ERROR (Database is not encrypted with supplied key)')

        drop_sessions()

    print("* Test complete!")
