# users view

from sqlalchemy import exc

from ..models.base import get_session
from ..models.User import User
from ..modules.carry import global_scope


def new_validation_key():
    """
        Create a validation key
    """

    key_salt = global_scope['enc'].key + \
        global_scope['conf'].salt.encode()

    # Save user
    user = User(key='key_validation',
                value=global_scope['enc'].encrypt(key_salt))
    get_session().add(user)
    get_session().commit()


def validate_validation_key(key):
    """
        Verify if a validation key is valid
    """

    # validation key from database
    try:
        user = get_session().query(User).filter(
            User.key == 'key_validation').order_by(User.id.desc()).first()
    except exc.DatabaseError:  # In case of encrypted db, if the encryption key is invalid
        return False

    # Concatenate user given key and config's salt
    key_salt = key + global_scope['conf'].salt.encode()

    # Key is valid
    try:
        if global_scope['enc'].decrypt(user.value) == key_salt:
            return True
    except ValueError:  # Decryption error
        return False

    return False
