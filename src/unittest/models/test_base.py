from unittest.mock import patch
import tempfile

from sqlalchemy import engine
from sqlalchemy.orm import Session

from ..base import BaseTest
from ...models import base
from ...modules.carry import global_scope


class Test(BaseTest):

    def test_get_session(self):
        self.assertIsInstance(base.get_session(), Session)

    def test_get_session_2(self):
        # Text exception with `db_file` is not defined
        with patch.dict(global_scope, {'db_file': None}):
            self.assertRaises(RuntimeError, base.get_session)

    def test_drop_sessions(self):
        self.assertTrue(base.drop_sessions())
        self.assertEqual(base.sessions, {})

    def test_get_engine(self):
        self.assertIsInstance(base.get_engine(), engine.base.Engine)

    def test_get_engine_2(self):
        # Text exception with `db_file` is not defined
        with patch.dict(global_scope, {'db_file': None}):
            self.assertRaises(RuntimeError, base.get_engine)

    def test_get_engine_3(self):
        # Test non-encrypted connection with a temporary file
        file_ = tempfile.NamedTemporaryFile()
        with patch.dict(global_scope, {'db_file': file_.name}):
            self.assertIsInstance(base.get_engine(False), engine.base.Engine)

    def test_get_db_key(self):
        self.assertIsInstance(base.get_db_key(), str)

    def test_get_db_key_2(self):
        # Text exception with `enc` is not defined
        with patch.dict(global_scope, {'enc': None}):
            self.assertRaises(RuntimeError, base.get_db_key)

    def test_get_db_key_3(self):
        # Text exception with `conf` is not defined
        with patch.dict(global_scope, {'conf': None}):
            self.assertRaises(RuntimeError, base.get_db_key)

    def test_get_slashes(self):
        with patch.dict(global_scope, {'db_file': '/foo/bar'}):
            self.assertEqual(base.get_slashes(encrypted=True), '//')

    def test_get_slashes_2(self):
        with patch.dict(global_scope, {'db_file': 'foo/bar'}):
            self.assertEqual(base.get_slashes(encrypted=True), '/')

    def test_get_slashes_3(self):
        with patch.dict(global_scope, {'db_file': '/foo/bar'}):
            self.assertEqual(base.get_slashes(encrypted=False), '////')

    def test_get_slashes_4(self):
        with patch.dict(global_scope, {'db_file': 'foo/bar'}):
            self.assertEqual(base.get_slashes(encrypted=False), '///')
