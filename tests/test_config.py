from diceware.config import OPTIONS_DEFAULTS


class TestConfigModule(object):
    # tests for diceware.config

    def test_defaults(self):
        # there is a set of defaults for options available
        assert OPTIONS_DEFAULTS is not None
