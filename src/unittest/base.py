import unittest
import tempfile
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.base import Base, get_session, get_engine
from ..models.User import UserModel
from ..lib.Config import Config
from ..lib.Encryption import Encryption
from ..modules.carry import global_scope


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set db location
        file_ = tempfile.NamedTemporaryFile(delete=False)
        global_scope['db_file'] = file_.name

        # Create a user key
        cls.secret_key = str(uuid.uuid4())
        cls.enc = global_scope['enc'] = Encryption(cls.secret_key.encode())

        # Load config
        cls.conf_path = tempfile.TemporaryDirectory()
        cls.config = Config(cls.conf_path.name + '/config')
        global_scope['conf'] = cls.config

        # Create engine
        engine = get_engine()

        # Create tables and set database session
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

        # Concatenate key and config's salt
        key_salt = cls.secret_key.encode(
        ) + global_scope['conf'].salt.encode()

        # Save user
        user = UserModel(key='key_validation',
                         value=cls.enc.encrypt(key_salt))
        cls.session.add(user)
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        # cls.session.remove()
        pass

        # Cleanup config directory
        cls.conf_path.cleanup()
