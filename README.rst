diceware
========

Passphrases to remember...

|bdg-build|  | `documentation <https://diceware.readthedocs.org/>`_ | `sources <https://github.com/ulif/diceware>`_ | `issues <https://github.com/ulif/diceware/issues>`_

.. |bdg-build| image:: https://travis-ci.org/ulif/diceware.png?branch=master
    :target: https://travis-ci.org/ulif/diceware
    :alt: Build Status

.. |bdg-last-release|  image:: https://pypip.in/version/diceware/badge.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: Latest Release

.. |bdg-versions| image:: https://pypip.in/py_versions/diceware/badge.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: Supported Python Versions

.. |bdg-license| image:: https://pypip.in/license/diceware/badge.svg
    :target: https://pypi.python.org/pypi/diceware/
    :alt: License

.. |doc-status| image:: https://readthedocs.org/projects/diceware/badge/?version=latest
     :target: https://diceware.readthedocs.org/en/latest/
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
  Create a passphrase
  
  positional arguments:
    INFILE                Input wordlist. `-' will read from stdin.
  
  optional arguments:
    -h, --help            show this help message and exit
    -n NUM, --num NUM     number of words to concatenate. Default: 6
    -c, --caps            Capitalize words. This is the default.
    --no-caps             Turn off capitalization.
    -s NUM, --specials NUM
                          Insert NUM special chars into generated word.
    -d DELIMITER, --delimiter DELIMITER
                          Separate words by DELIMITER. Empty string by default.
    -r SOURCE, --randomsource SOURCE
                          Get randomness from this source. Possible values:
                          `realdice', `system'. Default: system
    -w NAME, --wordlist NAME
                          Use words from this wordlist. Possible values: `en',
                          `en_orig'. Wordlists are stored in the folder
                          displayed below. Default: en
    --version             output version information and exit.


With ``-n`` you can tell how many words are supposed to be picked for
your new passphrase::

  $ diceware -n 1
  Thud

  $ diceware -n 2
  KnitMargo

You can `diceware` additionally let generate special chars to replace
characters in the 'normal' passphrase.  The number of special chars
generated can be determined with the ``-s`` option (*default is zero*)::

  $ diceware -s 2
  Heroic%unkLon#DmLewJohns

Here ``"%"`` and ``"#"`` are the special chars.

Special chars are taken from the following list::

  ~!#$%^&*()-=+[]\{}:;\"'<>?/0123456789

Please note that several special chars might replace the same original
char, resulting in a passphrase with less special chars than requested.

With ``-d`` you can advise `diceware` to put a delimiter string
between the words generated::

  $ diceware -d "_"
  Wavy_Baden_400_Whelp_Quest_Macon

By default we use the empty string as delimiter, which is good for
copying via double click on Linux systems. But other delimiters might
make your passphrases more readable.

By default the single phrase words are capitalized, i.e. the first
char of each word is made uppercase. This does not neccessarily give
better security (1 bit at most), but it helps reading a phrase.

You can nevertheless disable caps with the ``--no-caps`` option::

  $ diceware --no-caps
  oceanblendbaronferrylistenvalet

This leads to lower-case passphrases, maybe easier to type on smart
phones or similar.

`diceware` supports also different sources of randomness, which can be
chosen with the ``-r <SOURCENAME>`` or ``--randomsource <SOURCENAME>``
option. Use the ``--help`` option to list all valid values for this
option.

By default we use the `random.SystemRandom`_ class of standard Python
lib but you can also bring your own dice to create randomness::

  $ diceware -r realdice
  Please roll 5 dice (or a single dice 5 times).
  What number shows dice number 1? 2
  What number shows dice number 2? 3
  ...
  DogmaAnyShrikeSageSableHoar

We support even sources of randomness from other packages. See the
`documentation <https://diceware.readthedocs.org/>`_ for more details.

`diceware` comes with an English wordlist (the 'diceware8k' list)
provided by Arnold G. Reinhold, which will be used by default and
contains 8192 different words.

Apart from that `diceware` is packaged with the "original" 7776 word
list provided by Mr. Reinhold. You can enable a certain (installed)
wordlist with the ``-w`` option::

  $ diceware --wordlist en_orig
  YorkNodePrickEchoToriNiobe

See ``diceware --help`` for a list of all installed wordlists.

If you do not like the wordlists provided, you can use your own
one. Any `INFILE` provided will be parsed line by line and each line
considered a possible word. For instance::

  $ echo -e "hi\nhello\n" > mywordlist.txt
  $ diceware mywordlist.txt
  HelloHelloHiHiHiHello

With dash (``-``) as filename you can pipe in wordlists::

  $ echo -e "hi\nhello\n" > mywordlist.txt
  $ cat mywordlist.txt | diceware -
  HiHiHelloHiHiHello

In custom wordlists we take each line for a valid word and ignore
empty lines (i.e. lines containing whitespace characters only). Oh,
and we handle even PGP-signed wordlists.

You can set customized default values in a configuration file
``.diceware.ini`` (note the leading dot) placed in your home
directory. This file could look like this::

  [diceware]
  num = 7
  caps = off
  specials = 2
  delimiter = "MYDELIMITER"
  randomsource = "system"
  wordlist = "en"

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

The standard english wordlist of this `diceware` implementation
contains 8192 = 2**13 different english words. It is a copy of the
`Diceware8k list`_ provided by Mr. Reinhold. Therefore, picking a random word
from this list gives an entropy of 13 bits. Picking six words means an
entropy of 6 x 13 = 73 bits.

The special chars replacing chars of the originally created passphrase
give some more entropy (the more chars you have, the more additional
entropy), but not much. For instance, for a sixteen chars phrase you
have sixteen possibilities to place one of the 36 special chars. That
makes 36 x 16 possibilitities or an entropy of about 9.17 you can add.
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


Developer Install
-----------------

Developers want to `fork me on github`_::

  $ git clone https://github.com/ulif/diceware.git

We recommend to create and activate a virtualenv_ first::

  $ cd diceware/
  $ virtualenv -p /usr/bin/python3.3 py33
  $ source py33/bin/activate
  (py33) $

We support Python versions 2.6, 2.7, 3.2, 3.3, 3.4, pypy.

Now you can create the devel environment::

  (py33) $ python setup.py dev

This will fetch test packages (py.test_). You should be able to run
tests now::

  (py33) $ py.test

If you have also different Python versions installed you can use tox_
for using them all for testing::

  (py33) $ pip install tox   # only once
  (py33) $ tox

Should run tests in all supported Python versions.


Documentation Install
.....................

The docs can be generated with Sphinx_. The needed packages are
installed via::

  (py33) $ python setup.py docs

To create HTML you have to go to the ``docs/`` directory and use the
prepared ``Makefile``::

  (py33) $ cd docs/
  (py33) $ make

This should generate the docs in ``docs/_build/html/``.




Credits
-------

Arnold G. Reinhold deserves all merits for the working parts of
`Diceware`_. The non-working parts are certainly my fault.

People that helped spotting bugs, providing solutions, etc.:

 - `Conor Schaefer (conorsch) <https://github.com/conorsch>`_
 - Rodolfo Gouveia suggested to activate the ``--delimiter`` option.
 - `drebs <https://github.com/drebs>`_ provided patches and discussion for
   different sources of randomness.

Many thanks to all of them!


Links
-----

- The Diceware_ home page. Reading definitely recommended!
- `fork me on github`_

Wordlists:

- `Diceware8k list`_ by Arnold G. Reinhold.


License
-------

This Python implementation of Diceware, (C) 2015, 2016 Uli Fouquet, is
licensed under the GPL v3+.

The Copyright for the Diceware_ idea and the `Diceware8k list`_ are
Copyright by Arnold G. Reinhold. See file LICENSE for details.


.. _pip: https://pip.pypa.io/en/latest/
.. _`Diceware8k list`: http://world.std.com/~reinhold/diceware8k.txt
.. _`Diceware`: http://diceware.com/
.. _`fork me on github`: http://github.com/ulif/diceware/
.. _`random.SystemRandom`: https://docs.python.org/3.4/library/random.html#random.SystemRandom
.. _virtualenv: https://virtualenv.pypa.io/
.. _py.test: https://pytest.org/
.. _tox: https://tox.testrun.org/
.. _Sphinx: https://sphinx-doc.org/
