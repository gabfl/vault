# Secrets view

from ..models.base import get_session
from ..models.Secret import Secret


def all():
    """
        Return a list of all secrets
    """

    return get_session().query(Secret).order_by(Secret.id).all()


def count():
    """
        Return a count of all secrets
    """

    return get_session().query(Secret).count()
