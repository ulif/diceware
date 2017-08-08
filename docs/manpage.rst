:title: diceware
:title_upper: DICEWARE
:subtitle: create passphrases
:manual_section: 1
:manual_group: User Commands
:date: August 2017
:version: diceware 0.9.2.dev0
:author: Written by Uli Fouquet and contributors


synopsis
--------

``diceware`` [`OPTION`]... [`FILE`]


description
-----------

``diceware`` is a passphrase generator that generates passphrases by
concatenating words randomly picked from wordlists.

It is based on the proposals of Arnold G. Reinhold on http://diceware.com.


options
-------

``positional arguments``:

  INFILE
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
    Use words from this wordlist. Possible values: `en`,
    `en_8k`, `en_eff`, `en_orig`, `en_securedrop`.
    Wordlists are stored in the folder displayed below.
    Default: ``en_securedrop``

  ``-v``, ``--verbose``
    Be verbose. Use several times for increased verbosity.

  ``--version``
    output version information and exit.


copyright
---------

Copyright (C) 2015-2017 Uli Fouquet and contributors. License GPLv3+: GNU GPL
version 3 or later <https://gnu.org/licensesi/gpl.html>.

This is free software: you are free to change and redisttribute it.  There is
NO WARRANTY, to extent permitted by law.

