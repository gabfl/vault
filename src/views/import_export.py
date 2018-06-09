# Import/export view

import sys
import json

from tabulate import tabulate

from . import menu, secrets, categories
from ..modules.misc import confirm
from ..modules.carry import global_scope
from ..lib.Encryption import Encryption

"""
    Adding import or export formats:

    To add an import or export format, you need to add a file format name to
    `import_()` or `export()` and create an associated method
    called `import_from_[some_format]()` or `export_to[some_format]()`.

    The format name must also be added to `src/vault.py` in argparse choices.

    If you create a format that can be useful to others, please fork the project
    first and submit a merge request!
"""


def import_(format_, path):
    """
        Routing to format specific import methods
    """

    if format_ == 'json':
        return import_from_json(path)
    else:
        raise ValueError('%s is not a supported file format' % (format_))


def export_(format_, path):
    """
        Routing to format specific export methods
    """

    if format_ == 'json':
        return export_to_json(path)
    else:
        raise ValueError('%s is not a supported file format' % (format_))


def export_to_json(path):
    """
        Export to a Json file
    """

    # Ask user to unlock the vault
    unlock()

    # Create dict of secrets
    out = []
    for secret in secrets.all():
        out.append({
            'name': secret.name,
            'url': secret.url,
            'login': secret.login,
            'password': secret.password,
            'notes': secret.notes,
            'category': categories.get_name(secret.category_id),
        })

    return save_file(path, json.dumps(out))


def import_from_json(path=None, rows=None):
    """
        Import a Json file
    """

    # Ask user to unlock the vault (except if its already unlocked in migration)
    if not isinstance(global_scope['enc'], Encryption):
        unlock()

    if not rows:  # If importing from a file
        # Read content
        content = read_file(path)

        # Decode json
        rows = json.loads(content)

    # User view of items
    print("The following items will be imported:")
    print()
    print(to_table(
        [[row['name'], row['url'], row['login'], row['category']] for row in rows]))
    print()

    if confirm('Confirm import?', False):
        return import_items(rows)
    else:
        print("Import cancelled.")
        return False


def import_items(rows):
    """
        Import items at the following format:
        [{'name': '...', 'url': '...', 'login': '...', 'password': '...', 'notes': '...', 'category': '...'}]
    """

    for row in rows:
        # Set category ID
        category_id = None
        if row.get('category'):
            # Search within existing categories
            category_id = categories.get_id(row['category'])

            # Or create a new one
            if category_id is None:
                categories.add(name=row['category'])
                category_id = categories.get_id(row['category'])

        # Create secret
        secrets.add(name=row.get('name'),
                    url=row.get('url'),
                    login=row.get('login'),
                    password=row.get('password'),
                    notes=row.get('notes'),
                    category_id=category_id)

    print('%d items have been imported.' % len(rows))

    return True


def to_table(rows=[]):
    """
        Transform rows in a table
    """

    if len(rows) > 0:
        return tabulate(rows, headers=['Name', 'URL', 'Login', 'Category'])
    else:
        return 'Empty!'


def read_file(path, mode='r'):
    """
        Read an import file and return its content
    """

    # Read import file
    try:
        file = open(path, mode=mode)
        fileContent = file.read()
        file.close()

        return fileContent
    except Exception as e:
        print("The file `%s` could not be opened." % (path))
        print(e)
        sys.exit()


def save_file(path, content, mode='w'):
    """
        Save exported items to a file
    """

    # Save to file
    try:
        file = open(path, mode)
        file.write(content)
        file.close()

        print("The vault has been exported to the file `%s`." % (path))
    except Exception as e:
        print("The vault could not be exported to the file `%s`." % (path))
        print(e)

        return False

    return True


def unlock():
    """
        Ask user to unlock the vault
    """

    # `False` = don't load menu after unlocking
    return menu.unlock(redirect_to_menu=False)
