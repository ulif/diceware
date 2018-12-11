#  diceware -- passphrases to remember
#  Copyright (C) 2015-2017  Uli Fouquet and contributors.
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
import sys
import tempfile

#: Maximum in-memory file size in bytes (20 MB).
#:
#: This value is used when creating temporary files replacing
#: unseekable input streams. If an input file is larger, we write to
#: disk.
MAX_IN_MEM_SIZE = 20 * 1024 * 1024

#: A regular expression matching allowed wordlist names. We
#: allow names that cannot easily mess up filesystems.
RE_WORDLIST_NAME = re.compile(r'^[\w-]+$')

#: A regular expression matching numbered entries in wordlists.
RE_NUMBERED_WORDLIST_ENTRY = re.compile(r'^[0-9]+(\-[0-9]+)*\s+([^\s]+)$')

#: A regular expression describing valid wordlist file names.
RE_VALID_WORDLIST_FILENAME = re.compile(
    r'^wordlist_([\w-]+)\.[\w][\w\.]+[\w]+$')


def get_wordlists_dir():
    """Get the directory in which wordlsts are stored.
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'wordlists'))


def get_wordlist_names():
    """Get a all names of wordlists stored locally.
    """
    result = []
    wordlists_dir = get_wordlists_dir()
    filenames = os.listdir(wordlists_dir)
    for filename in filenames:
        if not os.path.isfile(os.path.join(wordlists_dir, filename)):
            continue
        match = RE_VALID_WORDLIST_FILENAME.match(filename)
        if not match:
            continue
        result.append(match.groups()[0])
    return sorted(result)


def get_wordlist_path(name):
    """Get path to a wordlist file for a wordlist named `name`.

    The `name` string must not contain special chars beside ``-``,
    ``_``, regular chars ``A-Z`` (upper or lower case) or
    numbers. Invalid names raise a ValueError.

    If a path with the given name (names are not filenames here) does
    not exist, `None` is returned.
    """
    if not RE_WORDLIST_NAME.match(name):
        raise ValueError("Not a valid wordlist name: %s" % name)
    wordlists_dir = get_wordlists_dir()
    for filename in os.listdir(wordlists_dir):
        if not os.path.isfile(os.path.join(wordlists_dir, filename)):
            continue
        match = RE_VALID_WORDLIST_FILENAME.match(filename)
        if match and match.groups()[0] == name:
            return os.path.join(wordlists_dir, filename)


class WordList(object):
    """A word list contains words for building passphrases.

    `path` is the path of the wordlist file. With single dash (``-``) as path,
    we read from `sys.stdin`.

    In case input comes from stdin, we write the input stream into a file if
    the content length is larger than `MAX_IN_MEM_SIZE`. Otherwise, the
    wordlist is kept in memory.

    Wordlist files are expected to contain words, one word per line. Empty
    lines are ignored, also whitespaces before or trailing a line are
    stripped. If a "word" contains inner whitespaces, then these are
    preserved.

    The input file can be a signed wordlist. Signed wordlists are expected to
    be ordinary lists of words but with ASCII armored signatures (as described
    in RFC 4880).

    In case of signed wordlists the signature headers/footers are stripped and
    the contained list of words is read.

    WordList are generators. That means, that you can retrieve the words of a
    wordlist by iterating over an instance of `WordList`.

    """
    def __init__(self, path):
        self.path = path
        self.fd = None
        if self.path == "-":
            self.fd = tempfile.SpooledTemporaryFile(
                    max_size=MAX_IN_MEM_SIZE, mode="w+")
            self.fd.write(sys.stdin.read())
            self.fd.seek(0)
        else:
            self.fd = open(self.path, "r")
        self.signed = self.is_signed()

    def __del__(self):
        if self.path != "-" and self.fd is not None:
            self.fd.close()

    def __iter__(self):
        self.fd.seek(0)
        if self.signed:
            while self.fd.readline().strip():
                # wait for first empty line
                pass
        for line in self.fd:
            line = self.refine_entry(line)
            if not line:
                continue
            elif self.signed and line == '-----BEGIN PGP SIGNATURE-----':
                break
            yield line

    def is_signed(self):
        """check, whether this file is cryptographically signed.

        This operation is expensive and resets the file descriptor to
        the beginning of file.
        """
        self.fd.seek(0)
        line1 = self.fd.readline()
        self.fd.seek(0)
        if line1.rstrip() == "-----BEGIN PGP SIGNED MESSAGE-----":
            return True
        return False

    def refine_entry(self, entry):
        """Apply modifications to form a proper wordlist entry.

        Refining means: strip() `entry` remove escape-dashes (if this is
        a signed wordlist) and extract the term if it is preceded by
        numbers.
        """
        if self.signed and entry.startswith('- '):
            entry = entry[2:]
        entry = entry.strip()
        match = RE_NUMBERED_WORDLIST_ENTRY.match(entry)
        if match:
            entry = match.groups()[1]
        return entry
