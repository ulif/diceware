import pytest
import sys


class InputMock(object):
    """A replacement for input() or raw_input() respectively.

    This mock, when called, mimics input() behaviour, outputs a prompt,
    etc., but does not wait for real key strokes. Instead it returns the
    next value from `fake_input_values` given on initialization:

       >>> faked_input = InputMock(["val1", "val2", "1"])
       >>> faked_input("Give a value: ")
       Give a value: val1
       'val1'

       >>> faked_input("And another value: ")
       And another value: val2
       'val2'

       >>> faked_input()
       1
       '1'

    To be used with the `monkeypatch` pytest fixture, to replace
    `diceware.random_sources.input_func`.
    """
    fake_input_values = []

    def __init__(self, fake_input_values=[]):
        self.fake_input_values = fake_input_values
        self.fake_input_values.reverse()

    def __call__(self, prompt=''):
        curr_value = self.fake_input_values.pop()
        print("%s%s" % (prompt, curr_value))
        return curr_value


@pytest.fixture(scope="function")
def argv_handler(request):
    """This fixture restores sys.argv and sys.stdin after tests.
    """
    _argv_stored = sys.argv
    _stdin_stored = sys.stdin

    def teardown():
        sys.argv = _argv_stored
        sys.stdin = _stdin_stored
    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def wordlists_dir(request, monkeypatch, tmpdir):
    """This fixture provides a temporary wordlist dir.
    """
    monkeypatch.setattr("diceware.wordlist.WORDLISTS_DIR", str(tmpdir))
    return tmpdir


@pytest.fixture(scope="function")
def home_dir(request, monkeypatch, tmpdir):
    """This fixture provides a temporary user home.
    """
    tmpdir.mkdir("home")
    monkeypatch.setenv("HOME", str(tmpdir / "home"))
    return tmpdir / "home"


@pytest.fixture(autouse=True)
def change_home(monkeypatch, tmpdir):
    """Set $HOME to some tempdir.

    This is an autouse fixture.

    If the user running tests has an own .diceware.ini in his home, then
    this will influence tests. Therefore we set the user home to some
    empty dir while tests are running.
    """
    monkeypatch.setenv("HOME", str(tmpdir))
    return tmpdir
