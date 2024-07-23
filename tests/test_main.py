#
# Tests for __main__.py
#
from diceware.__main__ import run
import pytest


def test_can_run_run(monkeypatch, capsys):
    # we can call __main__.py to run diceware
    monkeypatch.setattr("sys.argv", ["can_run_run", "--help"])
    monkeypatch.setattr("diceware.__main__.__name__", "__main__")
    with pytest.raises(SystemExit) as exc_info:
        run()
    assert exc_info.value.code == 0
    out, err = capsys.readouterr()
    assert "usage: can_run_run [-h]" in out


def test_run_respects_name(monkeypatch):
    # main() will only be called when __name__ == "__main__"
    monkeypatch.setattr("sys.argv", ["run_respects_name", "--help"])
    monkeypatch.setattr("diceware.__main__.__name__", "NOT__main__")
    try:
        run()
    except SystemExit:
        pytest.fail("running run() without proper __name__ raised SystemExit")
