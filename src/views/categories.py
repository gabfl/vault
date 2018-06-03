# Categories view

from ..models.base import get_session
from ..models.Category import Category
from ..models.Secret import Secret


def all():
    """
        Return a list of all categories
    """

    return get_session().query(Category).filter(Category.active == 1).all()


def exists(id):
    """
        Check if a category ID exists
    """

    if get_session().query(Category).filter(Category.id == int(id)).filter(Category.active == 1).first():
        return True

    return False


def get_name(id):
    """
        Get a category name from a category ID
    """

    cat = get_session().query(Category).filter(
        Category.id == int(id)).filter(Category.active == 1).first()

    if cat:
        return cat.name

    return False


def add(name):
    """
        Create a new category
    """

    cat = Category(name=name, active=1)
    get_session().add(cat)
    get_session().commit()

    return True


def rename(id, new_name):
    """
        Rename a category
    """

    cat = get_session().query(Category).filter(
        Category.id == int(id)).filter(Category.active == 1).first()

    if cat:
        cat.name = new_name
        get_session().add(cat)
        get_session().commit()

        return True

    return False


def delete(id):
    """
        Disable a category
    """

    cat = get_session().query(Category).filter(
        Category.id == int(id)).filter(Category.active == 1).first()

    if cat:
        cat.active = 0
        get_session().add(cat)
        get_session().commit()

        return True

    return False


def is_used(id):
    """
        Check if a category ID is used by any secret
    """

    if get_session().query(Secret).filter(
            Secret.category_id == int(id)).first():
        return True

    return False
