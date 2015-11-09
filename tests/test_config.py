from diceware.config import OPTIONS_DEFAULTS, valid_locations


class TestConfigModule(object):
    # tests for diceware.config

    def test_defaults(self):
        # there is a set of defaults for options available
        assert OPTIONS_DEFAULTS is not None

    def test_valid_locations(self, tmpdir, monkeypatch):
        # we look for config files in user home and local dir
        new_home = tmpdir / "home"
        new_home.ensure_dir()
        monkeypatch.setenv("HOME", str(new_home))
        assert valid_locations() == [
            str(new_home / ".diceware")
            ]
