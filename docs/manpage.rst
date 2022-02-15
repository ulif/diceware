:title: diceware
:title_upper: DICEWARE
:subtitle: create passphrases
:manual_section: 1
:manual_group: User Commands
:date: February 2022
:version: diceware 0.10
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
    optional input wordlist. ``'-'`` will read from stdin. Should contain one
    word per line.

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

  ``-w`` [`NAME` [`NAME` ...]], ``--wordlist`` [`NAME` [`NAME` ...]]
    Use words from this wordlist. Possible values: `de`, `de_8k`,
    `en_adjectives`, `en_eff`, `en_nouns`, `en_orig`, `en_securedrop`. `pt-br`.
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
    Use real dice to create a passphrase. The program will tell you what to do
    (roll dice and tell what numbers appear) and in the end present a
    passphrase.

``diceware -r`` `realdice` ``--dice-sides`` `20`
    Use real dice, as shown above, but this time use dice with 20 faces,
    instead of standard, 6-sided dice.

``diceware mywordlist.txt``
    Create a passphrase with words from file "mywordlist.txt". The file should
    contain one word on each line.

``diceware -w en_securedrop -s 2``
    Create a passphrase with two special chars spread over the generated
    passphrase and containing words from wordlist "``en_securedrop``". This is
    one of the wordlists that come included with `diceware`. Creates something
    like:
    "``PlayaBrigVer{SeesNe-tsGets``".

``diceware -w en_adjectives en_nouns -n 2``
    Create two syntactically meaningful phrases, each one consisting of an
    adjective and a noun. Results in something like:
    "``CruelAttendeesCleanCoffee``".

copyright
---------

Copyright (C) 2015-2022 Uli Fouquet and contributors

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.

diceware is a concept invented by Arnold G. Reinhold, Cambridge, Massachusetts
USA.

The Securedrop wordlist (file ``wordlists/wordlist_en_securedrop.asc``) by
Heartsucker is licensed under the `MIT` license (see http://mit-license.org/).

The EFF wordlist (file ``wordlsts/wordlist_en_eff.txt``) is licensed by the
Electronic Frontier Foundation under the `Creative Commons CC-BY 3.0 US`
license (see https://creativecommons.org/licenses/by/3.0/us/).


The copyright for the the `Diceware SecureDrop` list is owned by `@heartsucker`.
Copyright for the `EFF large` list by `Joseph Bonneau` and `EFF`. Copyright for
the brazilian portuguese list by `@drebs`. Copyright for the english adjective
and noun lists by `NaturalLanguagePasswords`.

"Diceware" is a trademark of Arnold G Reinhold, used with permission.
