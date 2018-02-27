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

    @pytest.mark.packaging
    def test_manpage_contains_current_year(self, manpage):
        # the current year appears at least in the manpage
        assert str(datetime.datetime.now().year) in manpage
