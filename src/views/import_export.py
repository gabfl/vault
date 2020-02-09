# Import/export view

import csv
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
    elif format_ == 'csv':
        return import_from_csv(path)
    else:
        raise ValueError('%s is not a supported file format' % (format_))


def export_(format_, path):
    """
        Routing to format specific export methods
    """

    if format_ == 'json':
        return export_to_json(path)
    elif format_ == 'csv':
        return export_to_csv(path)
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


def export_to_csv(path):
    """
        Export to a CSV file
    """

    # Ask user to unlock the vault
    unlock()

    # Create rows of secrets
    # NOTE: We are not using headers for now, it is disabled by default in KeePassXC csv import
    # TODO: ask maintainer if csv.DictReader is still preferred, or how how to handle this
    # keepassxc_headers = ['Group', 'Title', 'Username', 'Password', 'URL', 'Notes']
    # pyvault_headers = ['category', 'name', 'login', 'password', 'url', 'notes']
    rows = []
    for secret in secrets.all():
        rows.append([
            categories.get_name(secret.category_id),
            secret.name,
            secret.login,
            secret.password,
            secret.url,
            secret.notes,
        ])

    return save_file(path, rows, format_='csv')


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


def import_from_csv(path=None, rows=None):
    """
        Import a CSV file
    """

    # Ask user to unlock the vault (except if its already unlocked in migration)
    if not isinstance(global_scope['enc'], Encryption):
        unlock()

    if not rows:  # If importing from a file
        # Read content
        content = read_file(path, format_='csv')

        # Decode CSV
        reader = csv.reader(content)
        rows = list(reader)

        # Check if first rows contains `keepassxc_headers'
        keepassxc_headers = ['GROUP', 'TITLE', 'USERNAME', 'PASSWORD', 'URL', 'NOTES']
        if all([c.upper() in keepassxc_headers for c in rows[0]]):
            del rows[0]


    # TODO: csv.DictReader ?
    items = [{'category': row[0], 'name': row[1], 'login': row[2], 'password': row[3], 'url': row[4], 'notes': row[5]} for row in rows]
    # TODO: UNDO: KeePassXC includes "Root/" prefix that may(?) be desired
    for item in items:
        item['category'] = item['category'].split('/')[1]

    # User view of items
    print("The following items will be imported:")
    print()
    print(to_table(
        [[item['name'], item['url'], item['login'], item['category']] for item in items]))
    print()

    if confirm('Confirm import?', False):
        return import_items(items)
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


def read_file(path, mode='r', format_='json'):
    """
        Read an import file and return its content
    """

    # Read import file
    try:
        file = open(path, mode=mode)
        if format_ == 'csv':
            return file
        fileContent = file.read()
        file.close()

        return fileContent
    except Exception as e:
        print("The file `%s` could not be opened." % (path))
        print(e)
        sys.exit()


def save_file(path, content, mode='w', format_='json'):
    """
        Save exported items to a file
    """

    # Save to file
    try:
        file = open(path, mode)

        if format_ == 'json':
            file.write(content)
            file.close()
        else:
            writer = csv.writer(file)
            writer.writerows(content)

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
