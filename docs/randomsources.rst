Sources of Randomness
=====================

The security of your passphrase depends naturally heavily on the
source of randomness you use. If the source is good, it is really hard
to predict your passphrase. If it is bad, your passphrase might be
surprisingly easy to guess. `diceware` does not provide own
pseudo-random number generators or similar. Instead we let you choose
yourself the source of randomness you trust.

`diceware` supports different sources of randomness, which can be
chosen with the ``-r <SOURCENAME>`` or ``--randomsource <SOURCENAME>``
option.

Use the ``--help`` option to list all valid values for the
``--randomsource`` option.

Python-developers can provide their own source of randomness. If their
package is installed together with `diceware` (and their source is
registered correctly), `diceware` will offer their source as valid
option.


System Random
-------------

By default `diceware` uses the Python standard lib
:class:`random.SystemRandom` class to retrieve randomness. This class
calls an OS-specific source of randomness that returns data normally
unpredictable enough for our purposes. The quality of randomness
therefore depends on the quality of your OS implementation.

As a user you can enforce the use of this source of randomness with
the ``-r system`` option.

Please note that the Raspberry Pi is said to provide a hardware random
number generator that delivers "real randomness". One has to enable it
system-wide to make it the active source of randomness on a Raspberry
Pi. If done properly, also :class:`randomSystemRandom` (and hence
`diceware`) should use good quality random numbers.


Real Dice
---------

`diceware` also supports real dice as source of randomness. You can
pick this source of randomness with the ``-r realdice`` option.::

  $ diceware -r realdice
  Warning: entropy is reduced!
  Please roll 5 dice (or a single dice 5 times).
  What number shows dice number 1? 1
  What number shows dice number 2? 2
  What number shows dice number 3? 3
  What number shows dice number 4? 4
  What number shows dice number 5? 5
  Warning: entropy is reduced!
  Please roll 5 dice (or a single dice 5 times).
  What number shows dice number 1? 2
  What number shows dice number 2? 3
  What number shows dice number 3? 3
  What number shows dice number 4? 5
  What number shows dice number 5? 1

  ...

  What number shows dice number 5? 3
  AnyDogmaShrikeSageSableHoar

If you see a warning "entropy is reduced!", this means that not the
whole range of the wordlist you use can be put to account. Instead we
use (in case of 5 rolls) the first 6^5 words only. If you use a
wordlist with 6^n elements (for instance the original list with 7776
elements of Mr. Rheinhold), you will not get this warning.

Currently we support only 6-sided dice.


Bring Your Own Source (for developers)
--------------------------------------

`diceware` uses Python entry-points for looking up sources of
randomness. That means you can write your own source of randomness in
Python, register it in your own package and once both, your package
and `diceware` are installed together on a system, your source of
randomness will be offered and used by `diceware` (if the user selects
it).

To build your own source of randomness you have to provide a class
with a constructor that accepts a single `options` object. Furthermore
a source of randomness has to provide a `choice(sequence)` method. It
comes down to something like that::

  class MySourceOfRandomness(object):
      "Tell about your source..."
      def __init__(self, options):
          # initialize, etc.

      def choice(sequence):
          # return one of the elements in `sequence`

The `choice()` method will be called for each word of the passphrase
and for each special char. Please do not make assumptions about the
`sequence` passed to choice. It will be a list of "somethings" and be
indexable.

If your source is ready, you can register it in the ``setup.py`` of
your package like this::

    # setup.py

    ...

    setup(

        ...

        entry_points={
            'diceware_random_sources': [
              'mysrc = mypkg.sources:MySourceOfRandomness',
              # add more sources of randomness here...
            ],
        }
    )

Here we assume that you defined `MySourceOfRandomness` in a package
`mypkg` and a module called `sources`.

Once this package is installed, you can run `diceware` like this::

  $ diceware -r mysrc

and your source of randomness will be used.
