import unittest
import tempfile
import configparser

from ..base import BaseTest
from ...lib.Config import Config


class Test(BaseTest):

    def setUp(self):
        # Use a temporary file to test the config
        file_ = tempfile.NamedTemporaryFile()

        self.config = Config(file_.name)

    def test_getConfig(self):
        self.assertIsInstance(self.config.getConfig(),
                              configparser.SectionProxy)

    def test_setDefaultConfigFile(self):
        self.assertIsNone(self.config.setDefaultConfigFile())

    def test_update(self):
        self.config.update('some_name', 'some_value')
        retrieved = self.config.getConfig()
        self.assertEqual(retrieved['some_name'], 'some_value')

    def test_saveConfig(self):
        self.config.getConfig()
        self.assertIsNone(self.config.saveConfig())

    def test_generateRandomSalt(self):
        self.assertIsInstance(self.config.generateRandomSalt(), str)
