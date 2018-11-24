import re
import readline

# Usage:
#
# completion_list = ['suggestion', 'suggestion2', 'other_suggestion']
# result = get_input_autocomplete()
# print('Response -> ** % s**' % result)

completion_list = ['one', 'two', 'thee']


def autocomplete(text, state):
    """ Generic readline completion entry point. """

    buffer = readline.get_line_buffer()
    line = readline.get_line_buffer().split()

    # account for last argument ending in a space
    if re.compile(r'.*\s+$', re.M).match(buffer):
        line.append('')

    # resolve command to the implementation function
    cmd = line[0].strip()

    results = [c for c in completion_list if c.startswith(cmd)] + [None]

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
