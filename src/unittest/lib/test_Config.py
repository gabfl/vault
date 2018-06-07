import tempfile
import configparser

from ..base import BaseTest
from ...lib.Config import Config


class Test(BaseTest):

    def setUp(self):
        # Use a temporary file to test the config
        file_ = tempfile.NamedTemporaryFile()

        self.config = Config(file_.name)

    def test_get_config(self):
        self.assertIsInstance(self.config.get_config(),
                              configparser.SectionProxy)

    def test_set_default_config_file(self):
        self.assertIsNone(self.config.set_default_config_file())

    def test_update(self):
        self.config.update('some_name', 'some_value')
        retrieved = self.config.get_config()
        self.assertEqual(retrieved['some_name'], 'some_value')
        self.assertTrue(retrieved)

    def test_save_config(self):
        self.config.get_config()
        self.assertTrue(self.config.save_config())

    def test_generate_random_salt(self):
        self.assertIsInstance(self.config.generate_random_salt(), str)

    def test_getattr(self):
        self.assertIsInstance(self.config.salt, str)

    def test_getattr_2(self):
        self.assertIsNone(self.config.some_invalid_value)
