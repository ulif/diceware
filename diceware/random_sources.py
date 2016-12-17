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
"""Sources of randomness.

Please register all sources as entry point in ``setup.py``. Look out for
"SystemRandomSource" for an example.

For developers of interfaces to other sources of randomness: Currently,
you can extend `diceware` random sources by registering a class, that
provides a suitable `__init__(self, options)` and a `choice(self,
sequence)` method. Optionally, you can also provide a `classmethod`
called ``update_arparse`` that will get the possibility to update the
`argparser.ArgumentParser` used by `diceware`.

The `__init__` method of your class will be called with `options`, a set
of options as parsed from the commandline. The initialization code can
use the options to determine further actions or ignore it. The
`__init__` method is also the right place to ask users for one-time
infos you need. This includes infos like the number of sides of a dice,
an API key for random.org or other infos that should not change between
generating different words (but might change from one `diceware` call
to the next).

The `choice` method then, will get a sequence of chars, strings, or
numbers and should pick one of them based on the source of randomness
intended to be utilized by your code. If further user interaction is
required, `choice` might also ask users for input or similar. Typically,
`choice` is called once for each word and once for each special char to
generate.

If you want to manage own commandline options with your plugin, you can
implement a `classmethod` called ``update_argparser(parser)`` which gets
an `argparse.ArgumentParser` instance  as argument (no pun intended).

Finally, to register the source, add some stanza in `setup.py` of your
project that looks like::

    # ...
    setup(
        # ...
        entry_points={
            # console scripts and other entry points...
            'diceware_random_sources': [
                'myrandom = mypkg.mymodule:MyRandomSource',
                'myothersrc = mypkg.mymodule:MyOtherSource',
            ],
        },
        # ...
    )
    # ...

Here the `myrandom` and `myothersrc` lines register random sources that
(if installed) `diceware` will find on startup and offer to users under
the name given. In the described case, users could do for instance::

  diceware -r myrandom

and the random source defined in the given class would be used for
generating a passphrase.

"""
import math
import sys
from random import SystemRandom


input_func = input
if sys.version[0] < "3":
    input_func = raw_input  # NOQA  # pragma: no cover


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


class RealDiceRandomSource(object):
    """A source of randomness working with real dice.
    """
    def __init__(self, options):
        self.options = options
        self.dice_sides = 6
        if options is not None:
            self.dice_sides = getattr(options, 'dice_sides', 6)

    def pre_check(self, num_rolls, sequence):
        """Checks performed before picking an item of a sequence.

        We make sure that `num_rolls`, the number of rolls, is in an
        acceptable range and issue an hint about the procedure.
        """
        if num_rolls == 0:
            raise(ValueError)
        if (self.dice_sides ** num_rolls) < len(sequence):
            print(
                "Warning: entropy is reduced! Using only first %s of %s "
                "words/items of your wordlist." % (
                    self.dice_sides ** num_rolls, len(sequence)
                )
            )
        print(
            "Please roll %s dice (or a single dice %s times)." % (
                num_rolls, num_rolls))
        return

    def choice(self, sequence):
        """Pick one item out of `sequence`.
        """
        if len(sequence) == 1:
            return sequence[0]  # no need to roll dice.
        num_rolls = int(math.log(len(sequence), self.dice_sides))
        if num_rolls < 1:
            # If this happens, there are less values in the sequence to
            # choose from than there are dice sides.
            # Check whether len(sequence) is a factor of dice_sides
            if self.dice_sides % len(sequence) == 0:
                num_rolls = 1
            else:
                # otherwise We will perform one extra roll and apply modulo
                num_rolls = 2
        self.pre_check(num_rolls, sequence)
        result = 0
        for i in range(num_rolls, 0, -1):
            rolled = None
            while rolled not in [
                    str(x) for x in range(1, self.dice_sides + 1)]:
                rolled = input_func(
                    "What number shows dice number %s? " % (num_rolls - i + 1))
            result += ((self.dice_sides ** (i - 1)) * (int(rolled) - 1))
            result = result % len(sequence)
        return sequence[result]
