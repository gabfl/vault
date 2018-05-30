from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Session

from ..modules.carry import global_scope


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


def get_engine(encrypted=True):
    """
        return SQLAlchemy engine
    """

    if global_scope['db_file'] is None:
        raise RuntimeError('`db_file` is not defined in the global scope')

    if encrypted:
        return create_engine('sqlite+pysqlcipher://:testing@//' + global_scope['db_file'])
    else:
        return create_engine('sqlite:///' + global_scope['db_file'])
