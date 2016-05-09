import os
from diceware.config import (
    OPTIONS_DEFAULTS, valid_locations, get_configparser, get_config_dict,
    configparser,
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


class TestGetConfigDict(object):
    # tests for get_config_dict()

    def test_get_config_dict_no_config_file(self, home_dir):
        # we get config values even without a config file.
        conf_dict = get_config_dict()
        assert conf_dict == OPTIONS_DEFAULTS
        assert conf_dict is not OPTIONS_DEFAULTS

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

    def test_get_config_dict_arg_path_list(self, home_dir):
        # we can give the paths searched.
        config_file_default = home_dir / ".diceware.ini"
        config_file_default.write("[diceware]\nnum=4\n")
        config_file_custom = home_dir / "some-new-file"
        config_file_custom.write("[diceware]\nnum=42\n")
        conf_dict = get_config_dict(
            path_list=[str(config_file_custom), ])
        assert conf_dict['num'] == 42

    def test_get_config_dict_arg_defaults_dict(self, home_dir):
        # we can change the dict of defaults used.
        custom_defaults = dict(num=42)
        conf_dict = get_config_dict(defaults_dict=custom_defaults)
        assert conf_dict == dict(num=42)
        assert conf_dict is not custom_defaults

    def test_get_config_dict_arg_section(self, home_dir):
        # we can set the section name to look for in config files.
        config_file = home_dir / ".diceware.ini"
        config_file.write("[diceware]\nnum=4\n[foo]\nnum=5\n[bar]\nnum=6\n")
        conf_dict = get_config_dict(section='foo')
        assert conf_dict['num'] == 5

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

    def test_get_config_dict_string_quotes_stripped(self, home_dir):
        # preceding/trailing quotes are stripped from string values
        config_file = home_dir / ".diceware.ini"
        for string_in_conf, expected_parsed in (
                ('" "', " "), ("' '", " "), ('"\t\t"', "\t\t")):
            config_file.write("[diceware]\ndelimiter=%s \n" % string_in_conf)
            conf_dict = get_config_dict()
            assert conf_dict["delimiter"] == expected_parsed


class TestSampleIni(object):
    # test local sample ini file

    def test_complete_options_set(self, home_dir):
        # make sure the set of options in sample file is complete
        sample_path = os.path.join(
            os.path.dirname(__file__), 'sample_dot_diceware.ini')
        parser = configparser.SafeConfigParser()
        found = parser.read([sample_path, ])
        assert sample_path in found
        assert parser.has_section('diceware')
        for key, val in OPTIONS_DEFAULTS.items():
            # make sure option keywords are contained.
            assert parser.has_option('diceware', key)

    def test_no_invalid_options(self, home_dir):
        # ensure we have no obsolete/unused options in sample
        sample_path = os.path.join(
            os.path.dirname(__file__), 'sample_dot_diceware.ini')
        parser = configparser.SafeConfigParser()
        parser.read([sample_path, ])
        for option in parser.options('diceware'):
            assert option in OPTIONS_DEFAULTS.keys()
