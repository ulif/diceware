:title: diceware
:title_upper: DICEWARE
:subtitle: create passphrases
:manual_section: 1
:manual_group: User Commands
:date: December 2024
:version: diceware 1.0
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
    Use words from this wordlist. Possible values: `ca`, `de`, `de_8k`, `en`,
    `en_8k`, `en_adjectives`, `en_eff`, `en_nouns`, `en_orig`, `en_securedrop`.
    `es`, `it`, `pt-br`. Default: ``en_eff``

  ``-v``, ``--verbose``
    Be verbose. Use several times for increased verbosity.

  ``--version``
    output version information and exit.

``Arguments related to`` `realdice` ``randomsource``:

  ``--dice-sides`` `N`
    Number of sides of dice. Default: 6


environment variables
---------------------

``XDG_CONFIG_HOME``
    If set and not empty, this variable determines the directory to use for
    user-local configuration files. We then lookup
    `${XDG_CONFIG_HOME}/diceware/diceware.ini` and values set here override
    system-wide config files.

``XDG_CONFIG_DIRS``
    If set and not empty, this variable is interpreted as colon-separated list
    of directories, that might contain system-wide configuration files. We
    lookup `<DIR>/diceware/diceware.ini` for each directory set in
    `$XDG_CONFIG_DIRS`.

``XDG_DATA_HOME``
    If set and not empty, this variable determines a directory to search for
    additional wordlists. We then lookup `${XDG_DATA_HOME}/diceware` for any
    existing wordlist files.

 ``XDG_DATA_DIRS``
    If set and not empty, this variable is interpreted as colon-separated list
    of directories, that might contain additional wordlist files. See below. We
    lookup `<DIR>/diceware/` then for each directory set in the list.


files
-----

Depending on environment variables set (or not set) we lookup certain
directories for configuration files called ``diceware.ini`` and for wordlist
files.

CONFIGURATION FILES
...................

Configuration settings for ``diceware`` can be spread over several
configuration files. We parse configuration values from the files given below,
but values set in former files take precedence over values set in latter ones.

`~/.diceware.ini`
    Your personal diceware configuration file. Values set here override values
    from any other configuration file.

`$XDG_CONFIG_HOME/diceware/diceware.ini`
    Additional location for your personal diceware configuration. Values set
    here will override any system-wide valid values but can be overridden by
    `~/.diceware.ini`.

`$HOME/.config/diceware/diceware.ini`
    Alternative location for diceware configuration, only used if
    `${XDG_CONFIG_HOME}` is empty or unset.


`/etc/xdg/diceware/diceware.ini`
    If ``$XDG_CONFIG_DIRS`` is not set or empty, we look here for a system-wide
    configuration file. Values set here take least precedence.


WORDLIST FILES AND WORDLIST DIRECTORIES:
........................................

``diceware`` comes with a set of wordlists but enables you to add new wordlists
by putting them into certain directories. The paths where the lists are stored
(including the built-in ones) is shown using ``--show-wordlist-dirs``.

Wordlist files are expected to contain lines with one term on each
line and they must have a certain filenames to be found.

Wordlist filenames have to follow the pattern: ``wordlist_<NAME>.txt``
where ``<NAME>`` can be any name consisting of letters, numbers, underscores and
hyphens. For instance ``wordlist_en_eff.txt`` is the filename of the EFF
(electronic frontier foundation) word list. ``en_eff`` is the name of this list.

We support ``.txt`` and ``.asc`` as filename extensions for wordlists, where
``.txt`` files are expected to be plain wordlists and ``.asc`` files should
provide a PGP-signature.

If wordlists with the same name are found in different directories then the one
in the directory with the highest precedence is taken only. The following
locations are ordered by precedence (highest first). Therefore built-in
wordlists cannot be overridden by custom wordlists. You can, however, use
custom wordlists with a different name.

Directories we look up that do not exist (in part or completely) are silently
skipped when searching for wordlist files.

`<INSTALL-DIR>/wordlists/`
    The directory containing the built-in wordlists as part of the
    installation. These are the wordlists that are always available, regardless
    of configuration values and their exact location depends on the
    installation location of the ``diceware`` package.

`$XDG_DATA_HOME/diceware/`
    If $XDG_DATA_HOME is set and not empty, we look in this directory for
    wordlists.

`$HOME/.local/share/diceware/`
    If $XDG_DATA_HOME is unset or empty, we look  into this directory for
    wordlists.

`<DIR>/diceware` from `$XDG_DATA_DIRS`
    If $XDG_DATA_DIR is set and not empty, it is interpreted as a
    colon-separated list of directories with `/diceware` appended. So,
    `/foo/bar:/baz` will make us look into `/foo/bar/diceware/` and
    `/baz/diceware/` in that order.

`/usr/local/share/diceware/`, `/usr/share/diceware`
    If $XDG_DATA_DIRS is unset or empty, we look into these two directories for
    wordlists.

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

Copyright (C) 2015-2024 Uli Fouquet and contributors

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
