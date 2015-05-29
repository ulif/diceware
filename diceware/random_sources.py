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
"""Sources of randomness.

Please register all sources as entry point in ``setup.py``. Look out for
"SystemRandomSource" for an example.
"""
from random import SystemRandom


class SystemRandomSource(object):
    """A Random Source utilizing the standard Python `SystemRandom` call.

    As time of writing, SystemRandom makes use of ``/dev/urandom`` to get
    fairly useable random numbers.

    This source is registered as entry_point in setup.py under the name
    'system' in the ``diceware_random_sources`` group.

    The constructor will be called with options at beginning of a
    programme run if the user has chosen the respective source of
    random.

    The SystemRandomSource is the default source.
    """
    def __init__(self, options):
        self.options = options
        self.rnd = SystemRandom()

    def choice(self, sequence):
        """Pick one item out of `sequence`.

        The `sequence` will normally be a sequence of strings
        (wordlist), special chars, or numbers.

        Sequences can be (at least) lists, tuples and other types that
        have a `len`. Generators do not have to be supported (and are
        in fact not supported by this source).

        This method should return one item of the `sequence` picked based on
        the underlying source of randomness.

        In the long run, the choice should return each `sequence` item
        (i.e.: no items should be 'unreachable').

        It should also cope with any length > 0 of `sequence` and not
        break if a sequence is "too short" or "too long". Empty
        sequences, however, might raise exceptions.
        """
        return self.rnd.choice(sequence)
