# Categories view

from tabulate import tabulate

from ..models.base import get_session
from ..models.Category import Category
from ..models.Secret import Secret


def all():
    """
        Return a list of all categories
    """

    return get_session().query(Category).filter(Category.active == 1).order_by(Category.id).all()


def all_table():
    """
        Return a table of categories
    """

    # Retrieve id and name
    cats = [[cat.id, cat.name] for cat in all()]

    if len(cats) > 0:
        return tabulate(cats, headers=['Item', 'Category name'])
    else:
        return 'Empty!'


def exists(id_):
    """
        Check if a category ID exists
    """

    if get_session().query(Category).filter(Category.id == int(id_)).filter(Category.active == 1).first():
        return True

    return False


def get_name(id_):
    """
        Get a category name from a category ID
    """

    if not id_:
        return ''

    cat = get_session().query(Category).filter(
        Category.id == int(id_)).filter(Category.active == 1).first()

    if cat:
        return cat.name

    return ''


def add(name):
    """
        Create a new category
    """

    cat = Category(name=name, active=1)
    get_session().add(cat)
    get_session().commit()

    return True


def rename(id_, new_name):
    """
        Rename a category
    """

    cat = get_session().query(Category).filter(
        Category.id == int(id_)).filter(Category.active == 1).first()

    if cat:
        cat.name = new_name
        get_session().add(cat)
        get_session().commit()

        return True

    return False


def delete(id_):
    """
        Disable a category
    """

    cat = get_session().query(Category).filter(
        Category.id == int(id_)).filter(Category.active == 1).first()

    if cat:
        cat.active = 0
        get_session().add(cat)
        get_session().commit()

        return True

    return False


def is_used(id_):
    """
        Check if a category ID is used by any secret
    """

    if get_session().query(Secret).filter(
            Secret.category_id == int(id_)).first():
        return True

    return False
