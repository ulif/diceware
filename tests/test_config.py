from diceware.config import (
    OPTIONS_DEFAULTS, valid_locations, get_configparser, get_config_dict
    )


class TestConfigModule(object):
    # tests for diceware.config

    def test_defaults(self):
        # there is a set of defaults for options available
        assert OPTIONS_DEFAULTS is not None

    def test_valid_locations(self, home_dir):
        # we look for config files in user home and local dir
        assert valid_locations() == [
            str(home_dir / ".diceware.ini")
            ]

    def test_get_configparser(self, tmpdir):
        # we can parse simple configs
        conf_path = tmpdir / "sample.ini"
        conf_path.write("\n".join(["[diceware]", "num=1", ""]))
        found, config = get_configparser([str(conf_path), ])
        assert found == [str(conf_path)]

    def test_get_configparser_empty_list(self):
        # we cope with empty config file lists
        found, config = get_configparser([])
        assert found == []

    def test_get_configparser_no_list(self, home_dir):
        # we cope with no list at all
        found, config = get_configparser()
        assert found == []

    def test_get_configparser_default_path(self, home_dir):
        # a config file in $HOME is looked up by default
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[diceware]", "num = 3", ""]))
        found, config = get_configparser()
        assert found == [str(config_file)]

    def test_get_config_dict_no_config_file(self, home_dir):
        # we get config values even without a config file.
        conf_dict = get_config_dict()
        assert conf_dict == OPTIONS_DEFAULTS

    def test_get_config_dict_no_diceware_section(self, home_dir):
        # we cope with config files, if they do not contain a diceware config
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[not-diceware]", "num = 3", ""]))
        conf_dict = get_config_dict()
        assert conf_dict == OPTIONS_DEFAULTS

    def test_get_config_dict(self, home_dir):
        # we can get config values from files as a dict.
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[diceware]", "num = 3", ""]))
        conf_dict = get_config_dict()
        assert len(conf_dict) == len(OPTIONS_DEFAULTS)
        assert conf_dict != OPTIONS_DEFAULTS

    def test_get_config_dict_int(self, home_dir):
        # integer values are interpolated correctly
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[diceware]", "num=3", ""]))
        conf_dict = get_config_dict()
        assert "num" in conf_dict.keys()
        assert conf_dict["num"] == 3

    def test_get_config_dict_bool(self, home_dir):
        # boolean values are interpolated correctly
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[diceware]", "caps = Off", ""]))
        conf_dict = get_config_dict()
        assert "caps" in conf_dict.keys()
        assert conf_dict["caps"] is False
        config_file.write("\n".join(["[diceware]", "caps = On", ""]))
        assert get_config_dict()["caps"] is True

    def test_get_config_dict_ignore_irrelevant(self, home_dir):
        # values that have no default are ignored
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[diceware]", "foo = bar", ""]))
        conf_dict = get_config_dict()
        assert "foo" not in conf_dict.keys()

    def test_get_config_dict_string(self, home_dir):
        # string values are interpolated correctly
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[diceware]", "delimiter=!", ""]))
        conf_dict = get_config_dict()
        assert conf_dict["delimiter"] == "!"

    def test_get_config_dict_string_empty(self, home_dir):
        # we can set empty string values
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(["[diceware]", "delimiter=", ""]))
        conf_dict = get_config_dict()
        assert conf_dict["delimiter"] == ""
