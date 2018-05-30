# Categories view

from ..models.base import get_session
from ..models.Category import Category
from ..models.Secret import Secret

session = None


def local_session():
    """
        Maintain a session shared across all methods from this module
    """

    global session

    if session:
        return session

    session = get_session()
    return session


def all():
    """
        Return a list of all categories
    """

    return local_session().query(Category).filter(Category.active == 1).all()


def exists(id):
    """
        Check if a category ID exists
    """

    if local_session().query(Category).filter(Category.id == int(id)).filter(Category.active == 1).first():
        return True

    return False


def get_name(id):
    """
        Get a category name from a category ID
    """

    cat = local_session().query(Category).filter(
        Category.id == int(id)).filter(Category.active == 1).first()

    if cat:
        return cat.name

    return False


def add(name):
    """
        Create a new category
    """

    cat = Category(name=name, active=1)
    local_session().add(cat)
    local_session().commit()

    return True


def rename(id, new_name):
    """
        Rename a category
    """

    cat = local_session().query(Category).filter(
        Category.id == int(id)).filter(Category.active == 1).first()

    if cat:
        cat.name = new_name
        local_session().add(cat)
        local_session().commit()

        return True

    return False


def delete(id):
    """
        Disable a category
    """

    cat = local_session().query(Category).filter(
        Category.id == int(id)).filter(Category.active == 1).first()

    if cat:
        cat.active = 0
        local_session().add(cat)
        local_session().commit()

        return True

    return False


def is_used(id):
    """
        Check if a category ID is used by any secret
    """

    if local_session().query(Secret).filter(
            Secret.category_id == int(id)).first():
        return True

    return False
