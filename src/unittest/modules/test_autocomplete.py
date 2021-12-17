from unittest.mock import patch

from ..base import BaseTest
from ...modules import autocomplete


class Test(BaseTest):

    def test_set_parameters(self):
        autocomplete.set_parameters(
            list_=['four', 'five', 'six'],
            case_sensitive=False
        )

        assert autocomplete.completion_list == ['four', 'five', 'six']
        assert autocomplete.is_case_sensitive is False

    def test_autocomplete(self):
        autocomplete.set_parameters([
            'one_thing', 'one_other_thing', 'third_thing'])

        with patch('readline.get_line_buffer', return_value='one'):
            assert autocomplete.autocomplete('on', state=0) == 'one_thing'
            assert autocomplete.autocomplete(
                'on', state=1) == 'one_other_thing'
            assert autocomplete.autocomplete('on', state=2) is None

    def test_autocomplete_2(self):
        autocomplete.set_parameters([
            'one_thing', 'one_other_thing', 'third_thing'])

        with patch('readline.get_line_buffer', return_value='ONE'):
            assert autocomplete.autocomplete('on', state=0) is None

    def test_autocomplete_3(self):
        autocomplete.set_parameters(list_=[
            'one_thing', 'one_other_thing', 'third_thing'],
            case_sensitive=False)

        with patch('readline.get_line_buffer', return_value='ONE'):
            assert autocomplete.autocomplete('on', state=0) == 'one_thing'
            assert autocomplete.autocomplete(
                'on', state=1) == 'one_other_thing'
            assert autocomplete.autocomplete('on', state=2) is None

    def test_find_breaking_strings(self):

        assert autocomplete.find_breaking_strings('abc') == 0
        assert autocomplete.find_breaking_strings('abc@def') == 3
        assert autocomplete.find_breaking_strings('abc@def*ghi') == 7
        assert autocomplete.find_breaking_strings(
            'some@email.com somethingelse') == 14

    def test_get_input_autocomplete(self):
        autocomplete.set_parameters([
            'one_thing', 'one_other_thing', 'third_thing'])

        with patch('builtins.input', return_value='some_value'):
            assert autocomplete.get_input_autocomplete() == 'some_value'
