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

#: A regular expression matching numbered entries in wordlists.
RE_NUMBERED_WORDLIST_ENTRY = re.compile('^[0-9]+\s+([^\s]+)$')


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


def is_signed_wordlist(file_descriptor):
    """check, whether file in `file_descriptor` is signed.
    """
    line1 = file_descriptor.readline()
    file_descriptor.seek(0)
    if line1.rstrip() == "-----BEGIN PGP SIGNED MESSAGE-----":
        return True
    return False


def refine_wordlist_entry(entry, signed=False):
    """Apply modifications to form a proper wordlist entry.

    Set `signed` to `True` if the entry is part of a cryptographically
    signed wordlist.
    """
    if signed and entry.startswith('- '):
        entry = entry[2:]
    entry = entry.strip()
    match = RE_NUMBERED_WORDLIST_ENTRY.match(entry)
    if match:
        entry = match.groups()[0]
    return entry


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


def get_signed_wordlist(file_descriptor):
    """Parse cryptographically signed file in `file_descriptor` and
    build a wordlist out of it.

    `file_descriptor` is expected to be a file descriptor, already
    opened for reading. The descriptor will be closed after
    processing.

    Signed wordlists are expected to be wordlists as described in
    `get_wordlist()` but with ASCII armored signatures (as described in
    RFC 4880).

    The signature headers/footers are stripped and the contained list of
    words returned.
    """
    result = []
    while file_descriptor.readline().strip():
        # wait for first empty line
        pass
    for line in file_descriptor.readlines():
        line = refine_wordlist_entry(line, signed=True)
        if not line:
            continue
        elif line == '-----BEGIN PGP SIGNATURE-----':
            break
        result += [line, ]
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

try:
    basestring
except NameError:
    basestring = str


class WordList(object):
    """A word list contains words for building passphrases.

    `path_or_filelike` is the path of the wordlist file or an already
    opened file. Opened files must be open for reading, of course.
    """
    def __init__(self, path_or_filelike=None):
        self.path = None
        if isinstance(path_or_filelike, basestring):
            self.path = path_or_filelike
            self.fd = open(self.path, "r")
        else:
            self.fd = path_or_filelike
        self.signed = is_signed_wordlist(self.fd)
