import unittest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.base import Base, get_session
from ..models.User import User
from ..lib.Encryption import Encryption
from ..modules.carry import global_scope


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create all loaded models
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

        # Populate db
        cls.populate_base()

    @classmethod
    def populate_base(cls):
        """
            Populate the database
        """

        # Create a user key
        cls.secret_key = str(uuid.uuid4())
        cls.enc = global_scope[0] = Encryption((cls.secret_key).encode())

        # Save user
        user = User(key='key_validation',
                    value=cls.enc.encrypt(b'validation_string'))
        cls.session.add(user)
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        # cls.session.remove()
        pass
