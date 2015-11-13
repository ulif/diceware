import pytest
import sys


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
