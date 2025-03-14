diceware
========

Passphrases to remember...

|bdg-tests|  | `documentation <https://diceware.readthedocs.io/>`_ | `sources <https://github.com/ulif/diceware>`_ | `issues <https://github.com/ulif/diceware/issues>`_

.. |bdg-tests| image:: https://github.com/ulif/diceware/actions/workflows/tests.yml/badge.svg?branch=master
   :target: https://github.com/ulif/diceware/actions/workflows/tests.yml
   :alt: Test Status

.. |bdg-last-release| image:: https://img.shields.io/pypi/v/diceware.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: Latest Release

.. |bdg-versions| image:: https://img.shields.io/pypi/pyversions/diceware.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: Supported Python Versions

.. |bdg-license| image:: https://img.shields.io/pypi/l/diceware.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: License

.. |doc-status| image:: https://readthedocs.io/projects/diceware/badge/?version=latest
     :target: https://diceware.readthedocs.io/en/latest/
     :alt: Documentation Status

`diceware` is a passphrase generator following the proposals of
Arnold G. Reinhold on http://diceware.com . It generates passphrases
by concatenating words randomly picked from wordlists. For instance::

  $ diceware
  MyraPend93rdSixthEagleAid

The passphrase contains by default six words (with first char
capitalized) without any separator chars. Optionally you can let
`diceware` insert special chars into the passphrase.

`diceware` supports several sources of randomness (including real life
dice) and different wordlists (including cryptographically signed
ones).

.. contents::


Install
-------

This Python package can be installed via pip_::

  $ pip install diceware

The exact way depends on your operating system.


Usage
-----

Once installed, use ``--help`` to list all available options::

  $ diceware --help
  usage: diceware [-h] [-n NUM] [-c | --no-caps] [-s NUM] [-d DELIMITER]
                  [-r SOURCE] [-w [NAME [NAME ...]]] [--dice-sides N] [-v]
                  [--version]
                  [INFILE]

  Create a passphrase

  positional arguments:
    INFILE                Input wordlist. `-' will read from stdin.

  optional arguments:
    -h, --help            show this help message and exit
    -n NUM, --num NUM     number of words to concatenate. Default: 6
    -c, --caps            Capitalize words. This is the default.
    --no-caps             Turn off capitalization.
    -s NUM, --specials NUM
                          Append NUM special chars at the end of the generated
                          passphrase.
    -d DELIMITER, --delimiter DELIMITER
                          Separate words by DELIMITER. Empty string by default.
    -r SOURCE, --randomsource SOURCE
                          Get randomness from this source. Possible values:
                          `realdice', `system'. Default: system
    -w [NAME [NAME ...]], --wordlist [NAME [NAME ...]]
                          Use words from this wordlist. Possible values: `ca`,
                          `de', `de_8k', `en_adjectives', `en_eff', `en_nouns',
                          `en_securedrop', `es`, `fr`, `it`, `pt-br'.
                          Wordlists are stored in the folders displayed below.
                          Default: en_eff
    -v, --verbose         Be verbose. Use several times for increased verbosity.
    --version             output version information and exit.
    --show-wordlist-dirs  Output directories we look up to find wordlists and exit.

  Arguments related to `realdice' randomsource:
    --dice-sides N        Number of sides of dice. Default: 6

  Use --show-wordlist-dirs to list directories where you can store custom wordlists.

With ``-n`` you can tell how many words are supposed to be picked for
your new passphrase::

  $ diceware -n 1
  Runny

  $ diceware -n 2
  GroovyPostbox

You can `diceware` additionally let generate special chars, that will be
appended  to the 'normal' passphrase.  The number of special chars
generated can be determined with the ``-s`` option (*default is zero*)::

  $ diceware -s 2
  VioletParadoxImaginaryWheneverHarddiskOutburst%5

Here ``"%"`` and ``"5"`` are the special chars.

Special chars are randomly taken from the following list::

  ~!#$%^&*()-=+[]\{}:;\"'<>?/0123456789

Changed in: version 1.1.0. Until then the special chars were spread over the
generated passphrase, rendering it glibberish and harder to read and harder to
memorize.

With ``-d`` you can advise `diceware` to put a delimiter string
between the words generated::

  $ diceware -d "_"
  Wavy_Baden_400_Whelp_Quest_Macon

By default we use the empty string as delimiter, which is good for
copying via double click on Linux systems. But other delimiters might
make your passphrases more readable (and more secure, see
`Security Traps <#sec-traps>`_ below).

By default the single phrase words are capitalized, i.e. the first
char of each word is made uppercase. This does not necessarily give
better entropy (but protects against entropy loss due to non `prefix
code`_, see `Security Traps <#sec-traps>`_ below), and it might
improve phrase readability.

You can nevertheless disable caps with the ``--no-caps`` option::

  $ diceware --no-caps
  oceanblendbaronferrylistenvalet

This will leave the input words untouched (upper-case stays upper-case,
lower-case stays lower-case). It does *not* mean, that all output words will be
lower-case (except if all words of your wordlist are lowercase).

As the default lists of `diceware` contain only lower-case terms, here
``--no-caps`` means in fact lower-case only output, which might be easier to
type on smart phones and similar.

`diceware` supports also different sources of randomness, which can be
chosen with the ``-r <SOURCENAME>`` or ``--randomsource <SOURCENAME>``
option. Use the ``--help`` option to list all valid values for this
option.

By default we use the `random.SystemRandom`_ class of standard Python
lib but you can also bring your own dice to create randomness::

  $ diceware -r realdice --dice-sides 6
  Please roll 5 dice (or a single dice 5 times).
  Enter your 5 dice results, separated by spaces: 6 4 2 3 1
  Please roll 5 dice (or a single dice 5 times).
  Enter your 5 dice results, separated by spaces: 5 4 3 6 2
  ...
  UnleveledSimilarlyBackboardMurkyOasisReplay

Normally dice have six sides. And this is also the default in
`diceware` if you do not use ``--dice-sides``. But if you do, you can
tell how many sides (all) your dice have. More sides will lead to less
rolls required.

`diceware` comes with an English wordlist provided by the EFF_, which will be
used by default and contains 7776 (=6^5) different words. This list is
registered as ``en_eff``.

Additionally `diceware` comes with an English wordlist provided by
`@heartsucker`_, which contains 8192 different words. This list is based off
the original diceware list written by Arnold G. Reinhold.

You can enable a certain (installed) wordlist with the ``-w`` option::

  $ diceware --wordlist en_orig
  YorkNodePrickEchoToriNiobe

See ``diceware --help`` for a list of all installed wordlists.

You can also build phrases from adjectives and nouns (yet in english only)
using the included `en_adjectives` and `en_nouns` lists. For that you specify
these two wordlists after each other::

  $ diceware -n 1 -w en_adjectives en_nouns
  TediousPerimeter

These adjective/noun phrases might be easier to memorize.

If you do not like the wordlists provided, you can use your own
one. Any `INFILE` provided will be parsed line by line and each line
considered a possible word. For instance::

  $ echo -e "hi\nhello\n" > mywordlist.txt
  $ diceware mywordlist.txt
  HelloHelloHiHiHiHello

With dash (``-``) as filename you can pipe in wordlists::

  $ echo -e "hi\nhello\n" | diceware -
  HiHiHelloHiHiHello

In custom wordlists we take each line for a valid word and ignore
empty lines (i.e. lines containing whitespace characters only). Oh,
and we handle even PGP-signed wordlists.

You can set customized default values in a configuration file ``.diceware.ini``
(note the leading dot) placed in your home directory. Since version 1.0 you can
also use ``${XDG_CONFIG_HOME}/diceware/diceware.ini`` or
``${HOME}/.config/diceware/diceware.ini`` (if ``${XDG_CONFIG_HOME}`` is
undefined, see XDG_ for details).


This file could look like this::

  [diceware]
  num = 7
  caps = off
  specials = 2
  delimiter = "MYDELIMITER"
  randomsource = "system"
  wordlist = "en_securedrop"

The options names have to match long argument names, as output by
``--help``. The values set must meet the requirements valid for
commandline usage. All options must be set within a section
``[diceware]``.


What is it good for?
--------------------

Normally, `diceware` passphrases are easier to remember than shorter
passwords constructed in more or less bizarre ways. But at the same
time `diceware` passphrases provide more entropy as `xkcd`_ can show
with the famous '936' proof_:

.. image:: http://imgs.xkcd.com/comics/password_strength.png
   :align: center
   :target: http://xkcd.com/936/

.. _xkcd: http://xkcd.com/
.. _proof: http://xkcd.com/936/

The standard english wordlist of this `diceware` implementation contains 7776 =
6^5 different english words. It is the official EFF_ wordlist.  compiled by
`Joseph Bonneau`_. Therefore, picking a random word from this list gives an
entropy of nearly 12.9 bits. Picking six words means an entropy of 6 x 12.9 =
77.54 bits.

The special chars replacing chars of the originally created passphrase
give some more entropy (the more chars you have, the more additional
entropy), but not much. For instance, for a sixteen chars phrase you
have sixteen possibilities to place one of the 36 special chars. That
makes 36 x 16 possibilities or an entropy of about 9.17 you can add.
To get an entropy increase of at least 10 bits, you have to put a
special char in a phrase with at least 29 chars (while at the same
time an additional word would give you 13 bits of extra
entropy). Therefore you might think again about using special chars in
your passphrase.


Is it secure?
-------------

The security level provided by Diceware_ depends heavily on your
source of random. If the delivered randomness is good, then your
passphrases will be very strong. If instead someone can foresee the
numbers generated by a random number generator, your passphrases will
be surprisingly weak.

This Python implementation uses (by default) the
`random.SystemRandom`_ source provided by Python. On Un*x systems it
accesses `/dev/urandom`. You might want to follow reports about
manipulated random number generators in operating systems closely.

The Python API of this package allows usage of other sources of
randomness when generating passphrases. This includes real dice. See
the ``-r`` option.


.. _sec-traps:

Security Traps
--------------

There are issues that might reduce the entropy of the passphrase
generated. One of them is the `prefix code`_ problem:


Prefix Code
...........

If the wordlist contains, for example, the words::

   "air", "airport", "portable", "able"

*and* we switched off caps *and* delimiter chars, then `diceware` might
generate a passphrase containing::

   "airportable"

which could come from ``air-portable`` or ``airport-able``. We cannot
tell and an attacker would have less combinations to guess.

To avoid that, you can leave caps enabled (the default), use any word
delimiter except the empty string or use the ``en_eff`` wordlist,
which was checked to be a `prefix code`_ (i.e. it does not contain
words that start with other words in the list). The ``pt-br`` is also a secure
`prefix code`_.

Each of these measures is sufficient to protect you against the
`prefix code`_ problem.


Reduced Entropy
...............

Overall, `diceware` is a kind of mapping input values, dice throws for
instance, onto wordlist entries. We normally want each of the words in the
wordlist to be picked for passphrases with the same probability.

This, however, is not possible, if the number of wordlist entries is not a
power of dice sides. In that case we cut some words of the wordlist and inform
the user about the matter. Reducing the number of words this way makes it
easier for attackers to guess the phrase picked.

You can fix that problem by using longer wordlists.


Developer Install
-----------------

Developers want to `fork me on github`_::

  $ git clone https://github.com/ulif/diceware.git

We recommend to create and activate a virtualenv_ first::

  $ cd diceware/
  $ virtualenv -p /usr/bin/python3.11 py311
  $ source py311/bin/activate
  (py311) $

We support Python versions 2.7, 3.4 to 3.12, and pypy3.

Now you can create the devel environment::

  (py311) $ pip install '.[tests,dev]'

This will fetch test packages (py.test_), `ruff` as linter, `black` as code
formatter and `coverage`. You should be able to run tests now::

  (py311) $ pytest

If you have also different Python versions installed you can use tox_
for using them all for testing::

  (py311) $ pip install tox   # only once
  (py311) $ tox

Should run tests in all supported Python versions, the linter (`ruff`),
coverage tests and more.


Documentation Install
.....................

The docs can be generated with Sphinx_. The needed packages are
installed via::

  (py311) $ pip install '.[docs]'

To create the docs as HTML in a directory of your choice, then run::

   (py311) $ sphinx-build docs/ mydir/

You can also change to the ``docs/`` directory and use the prepared
``Makefile``::

  (py311) $ cd docs/
  (py311) $ make

This should generate the docs in ``docs/_build/html/``.


Creating the Man Page
.....................

We provide a `ReStructuredTexT`_ template to create a man page. When the
documentation engine is installed (`Sphinx`_, see above), then you can create a
manpage doing::

  (py311) $ rst2man.py docs/manpage.rst > diceware.1

The template is mainly provided to ease the job of Debian maintainers.
Currently, it is not automatically updated. Dates, authors, synopsis, etc. have
to be updated manually. Information in the manpage may therefore be wrong,
outdated, or simply misleading.


Credits
-------

Arnold G. Reinhold deserves all merits for the working parts of
`Diceware`_. The non-working parts are certainly my fault.

People that helped spotting bugs, providing solutions, etc.:

 - `Conor Schaefer (conorsch) <https://github.com/conorsch>`_
 - Rodolfo Gouveia suggested to activate the ``--delimiter`` option.
 - `@drebs`_ provided patches and discussion for different sources of
   randomness and the excellent ``pt-br`` wordlist. `@drebs`_ also initiated
   and performed the packaging of `diceware` for the `Debian`_ platform. Many
   kudos for this work! `@drebs`_ is also the official Debian maintainer of the
   `diceware` package.
 - `@heartsucker`_ hand-compiled and added a new english wordlist.
 - `dwcoder <https://github.com/dwcoder>`_ revealed and fixed bugs
   #19, #21, #23. Also showed sound knowledge of (theoretical)
   entropy. A pleasure to work with.
 - `George V. Reilly <https://github.com/georgevreilly>`_ pointed to new
   EFF wordlists.
 - `lieryan <https://github.com/lieryan>`_ brought up the `prefix
   code`_ problem.
 - `LogosOfJ <https://github.com/LogosOfJ>`_ discovered and fixed
   serious `realdice` source of randomness problem.
 - `Bhavin Gandhi <https://github.com/bhavin192>`_ fixed the confusing error
   message when an invalid input filename is given.
 - `Simon Fondrie-Teitler <https://github.com/simonft>`_ contributed a
   machine-readable copyright file, with improvements from `@anarcat`_
 - `Doug Muth <https://github.com/dmuth>`_ fixed formatting in docs.
 - `@kmille`_ suggested support for XDG config file locations.
 - `Tango` provided the french wordlist, also provided for `Tails OS`_ and the
   `Tor Project`_.
 - `@jawlenskys`_ provided the catalan, spanish and italian wordlists, also
   provided for `Tails OS`_ and the `Tor Project`_.

Many thanks to all of them!


Links
-----

- The Diceware_ home page. Reading definitely recommended!
- `fork me on github`_

External Wordlists:

- `Diceware standard list`_ by Arnold G. Reinhold.
- `Diceware8k list`_ by Arnold G. Reinhold.
- `Diceware SecureDrop list`_ by `@heartsucker`_.
- `EFF large list`_ provided by EFF_.
- `English adjectives and nouns lists`_ provided by `NaturalLanguagePasswords`_.


License
-------

This Python implementation of Diceware, (C) 2015-2024 Uli Fouquet, is
licensed under the GPL v3+. See file LICENSE for details.

"Diceware" is a trademark of Arnold G Reinhold, used with permission.

The copyright for the `Diceware8k list`_ is owned by Arnold G Reinhold.  The
copyright for the `Diceware SecureDrop list`_ are owned by `@heartsucker`_.
Copyright for the `EFF large list`_ by `Joseph Bonneau`_ and EFF_. Copyright
for the brazilian portuguese list by `@drebs`_. Copyright for the english
adjective and noun lists by `NaturalLanguagePasswords`_. See file COPYRIGHT for
details.

.. _pip: https://pip.pypa.io/en/latest/
.. _`@anarcat`: https://github.com/anarcat
.. _`Debian`: https://www.debian.org/
.. _`Diceware`: http://diceware.com/
.. _`Diceware standard list`: http://world.std.com/~reinhold/diceware.wordlist.asc
.. _`Diceware SecureDrop list`: https://github.com/heartsucker/diceware
.. _`Diceware8k list`: http://world.std.com/~reinhold/diceware8k.txt
.. _`@drebs`: https://github.com/drebs
.. _`EFF`: https://eff.org/
.. _`EFF large list`: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
.. _`English adjectives and nouns lists`: https://github.com/NaturalLanguagePasswords/system
.. _`fork me on github`: http://github.com/ulif/diceware/
.. _`@heartsucker`: https://github.com/heartsucker/
.. _`@jawlenskys`: https://github.com/jawlenskys
.. _`Joseph Bonneau`: https://www.eff.org/about/staff/joseph-bonneau
.. _`@kmille`: https://github.com/kmille
.. _`NaturalLanguagePasswords`: https://github.com/NaturalLanguagePasswords
.. _`prefix code`: https://en.wikipedia.org/wiki/Prefix_code
.. _`random.SystemRandom`: https://docs.python.org/3.4/library/random.html#random.SystemRandom
.. _`Tails OS`: https://tails.net/
.. _`Tor Project`: https://torproject.org/
.. _ReStructuredText: http://docutils.sourceforge.net/rst.html
.. _virtualenv: https://virtualenv.pypa.io/
.. _py.test: https://pytest.org/
.. _tox: https://tox.wiki/
.. _Sphinx: https://sphinx-doc.org/
.. _`XDG`: https://specifications.freedesktop.org/basedir-spec/latest/
