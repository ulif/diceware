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
    verbose=0,
    wordlist="en_securedrop",
    dice_sides=6,
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


def get_config_dict(
        path_list=None, defaults_dict=OPTIONS_DEFAULTS, section="diceware"):
    """Get config values found in files from `path_list`.

    Read files in `path_list` config files and return option values from
    section `section` as regular dictonary.

    We only accept values for which a default exists in
    `defaults_dict`. If `defaults_dict` is ``None`` we use
    ``OPTIONS_DEFAULTS``.

    Values are interpolated to have same value type as same-named values
    from `defaults_dict` if they are integers or boolean.

    String/text values are stripped from preceding/trailing quotes
    (single and double).
    """
    result = dict(defaults_dict)
    found, parser = get_configparser(path_list)
    for key, val in defaults_dict.items():
        if not parser.has_option(section, key):
            continue
        if isinstance(val, bool):
            result[key] = parser.getboolean(section, key)
        elif isinstance(val, int):
            result[key] = parser.getint(section, key)
        else:
            result[key] = parser.get(section, key).strip("\"'")
    return result
