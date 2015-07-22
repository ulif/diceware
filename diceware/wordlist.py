#  diceware -- passphrases to remember
#  Copyright (C) 2015  Uli Fouquet and contributors.
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
"""wordlist.py -- special handling of wordlists.
"""
import os
import re

#: The directory in which wordlists are stored
WORDLISTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'wordlists'))

#: A regular expression matching allowed wordlist names. We
#: allow names that cannot easily mess up filesystems.
RE_WORDLIST_NAME = re.compile('^[a-zA-Z0-9_-]+$')


def get_wordlist_names():
    """Get a all names of wordlists stored locally.
    """
    result = []
    filenames = os.listdir(WORDLISTS_DIR)
    for filename in filenames:
        if not os.path.isfile(os.path.join(WORDLISTS_DIR, filename)):
            continue
        if "_" not in filename:
            continue
        if "." not in filename:
            continue
        basename = filename.split(".")[0]
        name = basename.split("_", 1)[1]
        result.append(name)
    return sorted(result)


def get_wordlist(file_descriptor):
    """Parse file in `file_descriptor` and build a word list of it.

    `file_descriptor` is expected to be a file descriptor, already
    opened for reading. The descriptor will be closed after
    processing.

    A wordlist is expected to contain lines of words. Each line a
    word. Empty lines are ignored. Returns a list of terms (lines)
    found.
    """
    result = [
        line.strip() for line in file_descriptor.readlines()
        if line.strip() != '']
    file_descriptor.close()
    return result


def get_wordlist_path(name):
    """Get path to a wordlist file for a wordlist named `name`.

    The `name` string must not contain special chars beside ``-``,
    ``_``, regular chars ``A-Z`` (upper or lower case) or
    numbers. Invalid names raise a ValueError.
    """
    if not RE_WORDLIST_NAME.match(name):
        raise ValueError("Not a valid wordlist name: %s" % name)
    basename = 'wordlist_%s.txt' % name
    return os.path.join(WORDLISTS_DIR, basename)
