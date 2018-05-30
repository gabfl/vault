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

    def test_get_engine(self):
        self.assertIsInstance(base.get_engine(), engine.base.Engine)

    def test_get_engine_2(self):
        # Text exception with `db_file` is not defined
        with patch.dict(global_scope, {'db_file': None}):
            self.assertRaises(RuntimeError, base.get_engine)

    def test_get_engine_3(self):
        # Test encrypted connection with a temporary file
        file_ = tempfile.NamedTemporaryFile()
        with patch.dict(global_scope, {'db_file': file_.name}):
            self.assertIsInstance(base.get_engine(), engine.base.Engine)
