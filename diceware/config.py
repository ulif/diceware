#  diceware -- passphrases to remember
#  Copyright (C) 2015, 2016  Uli Fouquet
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""config -- diceware configuration

`diceware` is configurable via commandline, configuration files and
direct API calls.

"""
try:
    import configparser                  # Python 3.x
except ImportError:                      # pragma: no cover
    import ConfigParser as configparser  # Python 2.x
import os


OPTIONS_DEFAULTS = dict(
    num=6,
    caps=True,
    specials=0,
    delimiter="",
    randomsource="system",
    wordlist="en_securedrop",
    gpg_home=None,
    )


def valid_locations():
    """The list of valid paths we look up for config files.
    """
    user_home = os.path.expanduser("~")
    result = []
    if user_home != "~":
        result = [os.path.join(user_home, ".diceware.ini"), ]
    return result


def get_configparser(path_list=None):
    """Parse `path_list` for config values.

    If no list is given we use `valid_locations()`.

    Return a list of paths read and a config parser instance.
    """
    if path_list is None:
        path_list = valid_locations()
    parser = configparser.SafeConfigParser()
    found = parser.read(path_list)
    return found, parser


def get_config_dict(path_list=None):
    """Get config values found in files from `path_list`.

    Read files in `path_list` config files and return option valus as
    regular dictonary.

    We only accept values for which a default exists in
    `OPTIONS_DEFAULTS`.

    Values are interpolated to have same value type as same-named values
    from `OPTIONS_DEFAULTS` if they are integers or boolean.
    """
    result = dict(OPTIONS_DEFAULTS)
    found, parser = get_configparser(path_list)
    for key, val in OPTIONS_DEFAULTS.items():
        if not parser.has_option('diceware', key):
            continue
        if isinstance(val, bool):
            result[key] = parser.getboolean("diceware", key)
        elif isinstance(val, int):
            result[key] = parser.getint("diceware", key)
        else:
            result[key] = parser.get("diceware", key)
    return result
