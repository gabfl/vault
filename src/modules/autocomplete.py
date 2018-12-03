import re
import readline

# Usage:
#
# set_parameters(list_=['suggestion', 'suggestion2', 'other_suggestion'])
# result = get_input_autocomplete()
# print('Response -> ** % s**' % result)

completion_list = ['one', 'two', 'thee']
is_case_sensitive = True


def set_parameters(list_, case_sensitive=True):
    """ Set module parameters """

    global completion_list, is_case_sensitive

    completion_list = list_
    is_case_sensitive = case_sensitive


def autocomplete(text, state):
    """ Generic readline completion entry point. """

    buffer = readline.get_line_buffer()

    comp = completion_list
    if not is_case_sensitive:
        buffer = buffer.lower()
        comp = [c.lower() for c in completion_list]

    results = [c for c in comp if c.startswith(buffer)] + [None]

    # Handle multi-word inputs by truncating strings at the last space
    if buffer.find(' ') > 0:
        strip_pos = buffer.rfind(' ') + 1
        results = [i[strip_pos:] for i in results if i is not None] + [None]

    return results[state]


def get_input_autocomplete(message=''):
    """ Allow user to type input and provide auto-completion """

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    try:
        return input(message).strip()
    except KeyboardInterrupt:
        return False
    except Exception:  # Other Exception
        return False
