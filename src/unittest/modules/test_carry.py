from ..base import BaseTest
from ...lib.Encryption import Encryption
from ...lib.Config import Config
from ...modules.carry import global_scope


class Test(BaseTest):

    def test_enc(self):
        self.assertIsInstance(global_scope['enc'], Encryption)

    def test_db_file(self):
        self.assertIsInstance(global_scope['db_file'], str)

    def test_conf(self):
        self.assertIsInstance(global_scope['conf'], Config)
