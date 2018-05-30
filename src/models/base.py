from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Session


@as_declarative()
class Base(object):
    """
        Declarative base, shared with all models
    """

    pass


def get_session():
    """
        Return SQLAlchemy session
    """

    return Session(bind=get_engine())


def get_engine():
    """
        return SQLAlchemy engine
    """

    return create_engine('sqlite:///:memory:', echo=True)
