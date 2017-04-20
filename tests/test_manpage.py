import datetime
import os
import pytest


@pytest.fixture(scope="function")
def manpage(request):
    manpage_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'diceware.1')
    with open(manpage_path, 'r') as fd:
        content = fd.read()
    for token, replacement in [
            ('\\-', '-'), ('\\fB', ''), ('\\fR', '')]:
        content = content.replace(token, replacement)
    return content


class TestManpage(object):

    def test_manpage_contains_current_year(self, manpage):
        # the current year appears at least in the manpage
        assert str(datetime.datetime.now().year) in manpage

    def test_help_texts_in_manpage(self, manpage):
        # the text of help output appear in the manpage
        help_text_path = os.path.join(
            os.path.dirname(__file__), 'exp_help_output.txt')
        with open(help_text_path, 'r') as fd:
            help_text = fd.read()
        help_text = help_text.replace('<WORDLISTS-DIR>', '')
        for word in help_text.split():
            assert word in manpage
