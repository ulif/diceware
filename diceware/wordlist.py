#  diceware -- passphrases to remember
#  Copyright (C) 2015, 2016  Uli Fouquet and contributors.
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
import tempfile

#: Maximum in-memory file size in bytes (20 MB).
#:
#: This value is used when creating temporary files replacing
#: unseekable input streams. If an input file is larger, we write to
#: disk.
MAX_IN_MEM_SIZE = 20 * 1024 * 1024

#: The directory in which wordlists are stored
WORDLISTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'wordlists'))

#: A regular expression matching allowed wordlist names. We
#: allow names that cannot easily mess up filesystems.
RE_WORDLIST_NAME = re.compile('^[\w-]+$')

#: A regular expression matching numbered entries in wordlists.
RE_NUMBERED_WORDLIST_ENTRY = re.compile('^[0-9]+(\-[0-9]+)*\s+([^\s]+)$')

#: A regular expression describing valid wordlist file names.
RE_VALID_WORDLIST_FILENAME = re.compile(
    '^wordlist_([\w-]+)\.[\w][\w\.]+[\w]+$')


def get_wordlist_names():
    """Get a all names of wordlists stored locally.
    """
    result = []
    filenames = os.listdir(WORDLISTS_DIR)
    for filename in filenames:
        if not os.path.isfile(os.path.join(WORDLISTS_DIR, filename)):
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
    for filename in os.listdir(WORDLISTS_DIR):
        if not os.path.isfile(os.path.join(WORDLISTS_DIR, filename)):
            continue
        match = RE_VALID_WORDLIST_FILENAME.match(filename)
        if match and match.groups()[0] == name:
            return os.path.join(WORDLISTS_DIR, filename)


class WordList(object):
    """A word list contains words for building passphrases.

    `path_or_filelike` is the path of the wordlist file or an already
    opened file. Opened files must be open for reading, of course. We
    expect filelike objects to support at least `read()`.

    If a file-like object does not support `seek()` (like `sys.stdin`),
    we create a temporary, seekable copy of the input stream. The copy
    is written to disk only, if it is larger than
    `MAX_IN_MEM_SIZE`. Otherwise the wordlist is kept in memory.

    Please note that open file descriptors are not closed after reading.

    Wordlist files are expected to contain words, one word per
    line. Empty lines are ignored, also whitespaces before or trailing
    a line are stripped. If a "word" contains inner whitespaces, then
    these are preserved.

    The input file can be a signed wordlist. Signed wordlists are
    expected to be ordinary lists of words but with ASCII armored
    signatures (as described in RFC 4880).

    In case of signed wordlists the signature headers/footers are
    stripped and the contained list of words is read.

    WordList are generators. That means, that you can retrieve the
    words of a wordlist by iterating over an instance of `WordList`.

    """
    def __init__(self, path_or_filelike=None):
        self.path = None
        if not hasattr(path_or_filelike, 'read'):
            # got a path, not a filelike object
            self.path = path_or_filelike
            self.fd = open(self.path, "r")
        else:
            self.fd = path_or_filelike
            try:
                self.fd.seek(0)
            except IOError:
                # the given filelike does not support seek(). Create an own.
                self.fd = tempfile.SpooledTemporaryFile(
                    max_size=MAX_IN_MEM_SIZE, mode="w+")
                self.fd.write(path_or_filelike.read())
                self.fd.seek(0)
        self.signed = self.is_signed()

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
