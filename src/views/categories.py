# Categories view

import time

from tabulate import tabulate

from ..models.base import get_session
from ..models.Category import CategoryModel
from ..models.Secret import SecretModel
from ..modules.misc import confirm, clear_screen
from . import menu


def all():
    """
        Return a list of all categories
    """

    return get_session().query(CategoryModel).filter(CategoryModel.active == 1).order_by(CategoryModel.id).all()


def to_table(rows=[]):
    """
        Transform rows in a table
    """

    # Retrieve id and name
    cats = [[cat.id, cat.name] for cat in rows]

    if len(cats) > 0:
        return tabulate(cats, headers=['Item', 'Category name'])
    else:
        return 'Empty!'


def pick(message='Select a category: ', optional=False):
    """
        Ask a user to pick a category
    """

    all_categories = all()

    if len(all_categories) == 0:
        print()
        print('You did not create any category yet. You can create one from the main menu.')
        return False

    # Display available categories
    print()
    print(to_table(all_categories))
    print()

    # Ask user input
    id_ = menu.get_input(message=message)

    # Cast as int
    try:
        id_int = int(id_)
        if id_int and exists(id_int):
            return id_int
    except ValueError:  # Not a valid number!
        pass

    # No category picked
    if optional and id_ == '':
        return None

    print()
    print('Invalid category number!')

    return False


def exists(id_):
    """
        Check if a category ID exists
    """

    if get_session().query(CategoryModel).filter(CategoryModel.id == int(id_)).filter(CategoryModel.active == 1).first():
        return True

    return False


def get_name(id_):
    """
        Get a category name from a category ID
    """

    if not id_:
        return ''

    cat = get_session().query(CategoryModel).filter(
        CategoryModel.id == int(id_)).filter(CategoryModel.active == 1).first()

    if cat:
        return cat.name

    return ''


def get_id(name):
    """
        Get a category ID from a category name
    """

    if not name:
        return None

    cat = get_session().query(CategoryModel).filter(
        CategoryModel.name == name).filter(CategoryModel.active == 1).first()

    if cat:
        return cat.id

    return None


def add(name):
    """
        Create a new category
    """

    cat = CategoryModel(name=name, active=1)
    get_session().add(cat)
    get_session().commit()

    return True


def add_input():
    """
        Ask user for a category name and create it
    """

    # Ask user input
    name = menu.get_input(message='Category name: ')

    # Return false if name is missing
    if not name:
        return False

    # Create category
    result = add(name=name)

    print()
    print('The category has been created.')

    time.sleep(2)

    return result


def rename(id_, new_name):
    """
        Rename a category
    """

    cat = get_session().query(CategoryModel).filter(
        CategoryModel.id == int(id_)).filter(CategoryModel.active == 1).first()

    if cat:
        cat.name = new_name
        get_session().add(cat)
        get_session().commit()

        return True

    return False


def rename_input():
    """
        Rename a category
    """

    # Get id
    id_ = pick()

    # Return false if id is invalid
    if not id_:
        return False

    # Ask user input
    name = menu.get_input(message='Category name: ')

    # Return false if name is missing
    if not name:
        return False

    result = rename(id_, name)

    if result is True:
        print()
        print('The category has been renamed.')

        time.sleep(2)

    return result


def delete(id_):
    """
        Disable a category
    """

    cat = get_session().query(CategoryModel).filter(
        CategoryModel.id == int(id_)).filter(CategoryModel.active == 1).first()

    if cat:
        cat.active = 0
        get_session().add(cat)
        get_session().commit()

        return True

    return False


def delete_input():
    """
        Delete a category
    """

    # Get id
    id_ = pick()

    # Return false if id is invalid
    if not id_:
        return False

    # Return false if the category is used
    if is_used(id_):
        print()
        print(
            'The category cannot be deleted because it is currently used by some secrets.')
        return False

    if confirm('Confirm deletion of the category "' + get_name(id_) + '"?', False):
        result = delete(id_)

        if result is True:
            print()
            print('The category has been deleted.')

            time.sleep(2)

        return result

    return False


def is_used(id_):
    """
        Check if a category ID is used by any secret
    """

    if get_session().query(SecretModel).filter(
            SecretModel.category_id == int(id_)).first():
        return True

    return False


def main_menu():
    """
        Categories menu
    """

    while (True):
        # Clear screen
        clear_screen()

        # List categories
        print(to_table(all()))

        print()
        command = menu.get_input(
            message='Choose a command [(a)dd a category / (r)rename a category / (d)elete a category / (b)ack to Vault]: ',
            lowercase=True,
            non_locking_values=['l', 'q']
        )

        if command is False:
            print()

        # Action based on command
        if command == 'a':  # Add a category
            add_input()
            return
        elif command == 'r':  # Rename a category
            rename_input()
            return
        elif command == 'd':  # Delete a category
            delete_input()
            return
        elif command == 'b':  # Back to vault menu
            return
