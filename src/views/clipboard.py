import hashlib
import time

import pyperclip

from ..modules.carry import global_scope

clipboard_signature = None


def copy(to_copy, name='password', erase=False):
    """
        Copy an item to the clipboard
    """

    global clipboard_signature

    # Discard invalid input like `None` or empty strings
    if not erase and (type(to_copy) is not str or to_copy == ''):
        print('* Nothing to copy!')
        return False

    try:
        pyperclip.copy(to_copy)
    except pyperclip.PyperclipException:
        print('* Error: could not find a copy/paste mechanism for your system')
        return False

    if not erase:
        print('* The %s has been copied to the clipboard.' % (name))

    # Save signature
    clipboard_signature = get_signature(to_copy)


def is_changed():
    """
        Returns `True` if the clipboard content has changed
    """

    if clipboard_signature:
        return clipboard_signature != get_signature(pyperclip.paste())


def get_signature(item):
    """
        Returns the sha256 hash of a string
    """

    hash_object = hashlib.sha256(item.encode())
    return hash_object.hexdigest()


def wait():
    """
        Wait X seconds and erase the clipboard
    """

    if not clipboard_signature:
        return None

    print("* Clipboard will be erased in %s seconds" %
          (global_scope['conf'].clipboardTTL))

    try:
        # Loop until the delay is elapsed
        for i in range(0, int(global_scope['conf'].clipboardTTL)):
            print('.', end='', flush=True)
            time.sleep(1)  # Sleep 1 sec

            # Stop timer if clipboard content has changed
            if is_changed():
                break
    except KeyboardInterrupt as e:
        # Will catch `^-c` and immediately erase the clipboard
        pass

    print()
    erase()


def erase():
    """
        Erase clipboard content
    """

    global clipboard_signature

    if not is_changed():  # We will not empty the clipboard if its content has changed
        copy(to_copy='', erase=True)  # Empty clipboard
    clipboard_signature = ''  # Reset clipboard signature
