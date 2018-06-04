# Secrets view

from tabulate import tabulate

from ..models.base import get_session
from ..models.Secret import Secret
from ..views.categories import get_name as get_category_name


def all():
    """
        Return a list of all secrets
    """

    return get_session().query(Secret).order_by(Secret.id).all()


def all_table():
    """
        Return a table of secrets
    """

    # Retrieve id and name
    all_secrets = [[secret.id, get_category_name(secret.category_id), secret.name,
                    secret.url, secret.login] for secret in all()]

    if len(all_secrets) > 0:
        return tabulate(all_secrets, headers=['Item', 'Category', 'Name', 'URL', 'Login'])
    else:
        return 'Empty!'


def count():
    """
        Return a count of all secrets
    """

    return get_session().query(Secret).count()
