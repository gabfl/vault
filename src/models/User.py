from .base import Base

from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

    def __repr__(self):
        return "<UserModel(id='%s', key='%s', value='%s')>" % (
            self.id, self.key, self.value)
