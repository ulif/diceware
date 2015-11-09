#  diceware -- passphrases to remember
#  Copyright (C) 2015  Uli Fouquet
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
    wordlist="en_8k",
    )


def valid_locations():
    """The list of valid paths we look up for config files.
    """
    user_home = os.path.expanduser("~")
    result = []
    if user_home != "~":
        result = [os.path.join(user_home, ".diceware"), ]
    return result


class DicewareConfigParser(configparser.SafeConfigParser):
    pass
