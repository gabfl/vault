# users view

from sqlalchemy import exc

from ..models.base import get_session, drop_sessions
from ..models.User import UserModel
from ..modules.carry import global_scope


def validation_key_new():
    """
        Create a validation key
    """

    key_salt = global_scope['enc'].key + \
        global_scope['conf'].salt.encode()

    # Save user
    user = UserModel(key='key_validation',
                     value=global_scope['enc'].encrypt(key_salt))
    get_session().add(user)
    get_session().commit()


def validation_key_validate(key):
    """
        Verify if a validation key is valid
    """

    # validation key from database
    try:
        user = get_session().query(UserModel).filter(
            UserModel.key == 'key_validation').order_by(UserModel.id.desc()).first()
    except exc.DatabaseError:  # In case of encrypted db, if the encryption key is invalid
        # Drop db sessions to force a re-connection with the new key
        drop_sessions()

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


def validation_key_rekey(newenc):
    """
        Replace a validation key with a new master key
    """

    # Get validation key
    user = get_session().query(UserModel).filter(
        UserModel.key == 'key_validation').order_by(UserModel.id.desc()).first()

    if user:
        key_salt = newenc.key + \
            global_scope['conf'].salt.encode()

        # Update validation key
        user.value = newenc.encrypt(key_salt)

        get_session().add(user)
        get_session().commit()

        return True

    return False
