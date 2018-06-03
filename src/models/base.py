import hashlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Session

from ..modules.carry import global_scope


sessions = {}


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

    global sessions

    if global_scope['db_file'] is None:
        raise RuntimeError('`db_file` is not defined in the global scope')

    # Create a unique key for the db session
    db_file = global_scope['db_file']

    # Add a session to the current list
    if not sessions.get(db_file):
        sessions[db_file] = Session(bind=get_engine())

    return sessions[db_file]


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
