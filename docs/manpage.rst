:title: diceware
:title_upper: DICEWARE
:subtitle: create passphrases
:manual_section: 1
:manual_group: User Commands
:date: September 2017
:version: diceware 0.9.2
:author: Written by Uli Fouquet and contributors


synopsis
--------

``diceware`` [`OPTION`]... [`FILE`]


description
-----------

``diceware`` generates passphrases by concatenating words randomly picked from
wordlists. It supports also real dice for passphrase generation.

It is based on the proposals of Arnold G. Reinhold on http://diceware.com.


options
-------

``positional arguments``:

  FILE
    input wordlist. ``'-'`` will read from stdin.

``optional arguments``:

  ``-h``, ``--help``
    show help message and exit

  ``-n`` `NUM`, ``--num`` `NUM`
    number of words to concatenate. Default 6

  ``-c``, ``--caps``
    Capitalize words. This is the default.

  ``--no-caps``
    Turn off capitalization.

  ``-s`` `NUM`, ``--specials`` `NUM`
    Insert NUM special chars into generated word.

  ``-d`` `DELIMITER`, ``--delimiter`` `DELIMITER`
    Separate words by DELIMITER. Empty string by default.

  ``-r`` `SOURCE`, ``--randomsource`` `SOURCE`
    Get randomness from this source. Possible values:
    ``realdice``, ``system``. Default: ``system``

  ``-w`` `NAME`, ``--wordlist`` `NAME`
    Use words from this wordlist. Possible values: `en`, `en_eff`, `en_orig`,
    `en_securedrop`.  Wordlists are stored in the folder displayed below.
    Default: ``en_eff``

  ``-v``, ``--verbose``
    Be verbose. Use several times for increased verbosity.

  ``--version``
    output version information and exit.

``Arguments related to`` `realdice` ``randomsource``:

  ``--dice-sides`` `N`
    Number of sides of dice. Default: 6


files
-----

`~/.diceware.ini`
    Your personal diceware configuration file.

``diceware`` also comes with a set of wordlists. The path where these lists are
stored is showed with ``--help``.


examples
--------

``diceware``
    Create a passphrase using defaults. Outputs something like
    "``WheelDyeHonkCanvasWitsPuck``"

``diceware -d`` `"-"` ``-n`` `3`
    Create a passphrase with three words, separated by dash ("`-`"). Results in
    something like "``Wheel-Dye-Honk``"

``diceware --no-caps``
    Create a passphrase without capital words. Creates something like
    "``wheel-dye-honk``".

``diceware -r`` `realdice`
    Use real dice to create a passphrase. The programm will tell you what to do
    (roll dice and tell what numbers appear) and in the end present a
    passphrase.


copyright
---------

.. include:: ../COPYRIGHT

