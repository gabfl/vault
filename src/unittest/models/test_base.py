import unittest

from sqlalchemy import engine
from sqlalchemy.orm import Session

from ..base import BaseTest
from ...models import base


class Test(BaseTest):

    def test_get_session(self):
        self.assertIsInstance(base.get_session(), Session)

    def test_get_engine(self):
        self.assertIsInstance(base.get_engine(), engine.base.Engine)
