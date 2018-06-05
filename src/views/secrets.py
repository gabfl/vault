# Secrets view

from sqlalchemy import or_
from tabulate import tabulate

from ..models.base import get_session
from ..models.Secret import Secret
from ..views.categories import get_name as get_category_name
from ..modules.misc import get_input


def all():
    """
        Return a list of all secrets
    """

    return get_session().query(Secret).order_by(Secret.id).all()


def to_table(rows=[]):
    """
        Transform rows in a table
    """

    # Retrieve id and name
    all_secrets = [[secret.id, get_category_name(secret.category_id), secret.name,
                    secret.url, secret.login] for secret in rows]

    if len(all_secrets) > 0:
        return tabulate(all_secrets, headers=['Item', 'Category', 'Name', 'URL', 'Login'])
    else:
        return 'Empty!'


def count():
    """
        Return a count of all secrets
    """

    return get_session().query(Secret).count()


def get_by_id(id_):
    """
        Get a secret by ID
    """

    return get_session().query(Secret).get(int(id_))


def search(query):
    """
        Search by keyword
    """

    query = '%' + str(query) + '%'

    return get_session().query(Secret) \
        .filter(or_(Secret.name.like(query), Secret.url.like(query), Secret.login.like(query))) \
        .order_by(Secret.id).all()


def search_dispatch(query):
    """
        Run a user search. If the query is an integer we will first search by id, otherwise,
        it will be a keyword based search
    """

    if type(query) is int or query.isdigit():
        # Search an ID matching the input
        row = get_by_id(int(query))

        if row:
            return [row]

    # Otherwise return search result
    return search(query)


def search_input():
    """
        Ask user to input a search query
    """

    # Ask user input
    query = get_input(message='Enter search: ')

    if not query:
        print()
        print('Empty search!')
        return False

    # To prevent fat-finger errors, the search menu will also respond to common commands
    if query in ['s', 'a', 'l', 'q']:  # Common commands
        return query
    elif query == 'b':  # Return to previous menu
        return False

    # Get results
    results = search_dispatch(query)

    if len(results) == 1:  # Exactly one result
        return get(results[0].id)
    elif len(results) > 1:  # More than one result
        return search_results(results)
    else:
        print('No results!')
        return False


def search_results(rows):
    """
        Display search results
    """

    print(to_table(rows))

    # Ask user input
    input_ = get_input(
        message='Select a result # or type any key to go back to the main menu: ')

    if input_:
        try:
            result = [row for row in rows if row.id == int(input_)]

            if result:
                return get(result[0].id)
        except ValueError:  # Non integer
            pass

    return False


def get(id_):
    """
        Show a secret
    """
