from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base
from ..modules.carry import global_scope


class SecretModel(Base):
    __tablename__ = 'secrets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    login = Column(String)
    _password = Column(String)
    _notes = Column(BLOB)
    _salt = Column(String)
    category_id = Column(Integer)

    def __init__(self, name, url='', login='', password='', notes='', category_id=None):
        # Set class level vars
        self.salt = ''  # Will call the setter and set a salt automatically
        self.name = name
        self.url = url
        self.login = login
        self.password = password
        self.notes = notes
        self.category_id = category_id

    def __repr__(self):
        return "<SecretModel(id='%s', name='%s', login='%s', salt='%s')>" % (
            self.id, self.name, self.login, self._salt)

    def get_enc(self):
        """ Returns a shared instance of Encryption class """

        if global_scope['enc'] is None:
            raise RuntimeError('`enc` is not defined in the global scope.')

        return global_scope['enc']

    @hybrid_property
    def salt(self):
        """ `salt` getter """

        return self._salt

    @salt.setter
    def salt(self, void=''):
        """ `salt` setter """

        self._salt = self.get_enc().gen_salt()

    @hybrid_property
    def password(self):
        """ `password` getter """

        self.get_enc().set_salt(self.salt)
        return self.get_enc().decrypt(self._password).decode('utf-8')

    @password.setter
    def password(self, password):
        """ `password` setter """

        self.get_enc().set_salt(self.salt)
        self._password = self.get_enc().encrypt(password.encode())

    @hybrid_property
    def notes(self):
        """ `notes` getter """

        self.get_enc().set_salt(self.salt)
        return self.get_enc().decrypt(self._notes).decode('utf-8')

    @notes.setter
    def notes(self, notes):
        """ `notes` setter """

        self.get_enc().set_salt(self.salt)
        self._notes = self.get_enc().encrypt(notes.encode())
