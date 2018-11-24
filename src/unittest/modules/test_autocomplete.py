from unittest.mock import patch

from ..base import BaseTest
from ...modules import autocomplete


class Test(BaseTest):

    def test_autocomplete(self):
        autocomplete.completion_list = [
            'one_thing', 'one_other_thing', 'third_thing']

        with patch('readline.get_line_buffer', return_value='one'):
            assert autocomplete.autocomplete('on', state=0) == 'one_thing'
            assert autocomplete.autocomplete(
                'on', state=1) == 'one_other_thing'
            assert autocomplete.autocomplete('on', state=2) is None

    def test_get_input_autocomplete(self):
        autocomplete.completion_list = [
            'one_thing', 'one_other_thing', 'third_thing']

        with patch('builtins.input', return_value='some_value'):
            assert autocomplete.get_input_autocomplete() == 'some_value'
