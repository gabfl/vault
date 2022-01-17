import os
from unittest.mock import patch
from tempfile import NamedTemporaryFile

import sqlcipher3
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..base import BaseTest
from ...lib.Encryption import Encryption
from ...lib.Config import Config
from ...modules.carry import global_scope
from ...tools import troubleshoot_db


class Test(BaseTest):

    def test_load_config(self):
        # Preserve global scope
        save = global_scope['conf']

        troubleshoot_db.load_config()
        assert isinstance(global_scope['conf'], Config)

        # Restore global scope
        global_scope['conf'] = save

    def test_set_vault_path(self):
        # Preserve global scope
        save = global_scope['enc']

        troubleshoot_db.set_vault_path()
        assert isinstance(global_scope['db_file'], str)

        # Restore global scope
        global_scope['enc'] = save

    def test_get_key_input(self):
        with patch('getpass.getpass', return_value='some input'):
            assert troubleshoot_db.get_key_input() == 'some input'

    def test_set_encryption(self):
        # Preserve global scope
        save = global_scope['enc']

        troubleshoot_db.set_encryption('test')
        assert isinstance(global_scope['enc'], Encryption)
        assert global_scope['enc'].key == 'test'.encode()

        # Restore global scope
        global_scope['enc'] = save

    def test_get_pragma_key(self):
        # Preserve global scope
        save = global_scope['enc']

        troubleshoot_db.set_encryption('test')
        pragma = troubleshoot_db.get_pragma_key()
        assert isinstance(pragma, str)
        assert len(pragma) == 64

        # Restore global scope
        global_scope['enc'] = save

    def test_query_vault_db(self):
        # Test with encrypted (default) database
        res = troubleshoot_db.query_vault_db()
        assert res is True

        # Preserve global scope
        save = global_scope['db_file']

        # Create an encrypted database with a dummy key
        f = NamedTemporaryFile(delete=False)
        engine = create_engine(
            'sqlite+pysqlcipher://:abcd@//' + f.name, module=sqlcipher3)
        connection = engine.connect()
        connection.execute('CREATE TABLE foo (a int)')

        global_scope['db_file'] = f.name

        res = troubleshoot_db.query_vault_db()
        assert res is False

        # Restore global scope
        global_scope['db_file'] = save

    def test_create_temporary_file(self):
        temp_file = troubleshoot_db.create_temporary_file()
        assert os.path.isfile(temp_file)

    def test_create_temporary_secret(self):
        secret = troubleshoot_db.create_temporary_secret()
        assert isinstance(secret, str)
        assert len(secret) == 32

    def test_attempt_dummy_encrypted_db(self):
        db_path = troubleshoot_db.create_temporary_file()
        assert troubleshoot_db.attempt_dummy_encrypted_db(db_path) is True

    def test_verify_if_dummy_db_is_encrypted(self):
        # Test with encrypted database
        db_path = troubleshoot_db.create_temporary_file()
        troubleshoot_db.attempt_dummy_encrypted_db(db_path)
        res = troubleshoot_db.verify_if_dummy_db_is_encrypted(db_path)
        assert res is True

        # Test with unencrypted database
        db_path = troubleshoot_db.create_temporary_file()
        engine = create_engine('sqlite:///' + db_path)
        res = troubleshoot_db.verify_if_dummy_db_is_encrypted(db_path)
        assert res is False
