diceware
========

Passphrases to remember...

|build-status|_

.. |build-status| image:: https://travis-ci.org/ulif/diceware.png?branch=master
.. _build-status: https://travis-ci.org/ulif/diceware


`diceware` is a password generator following the proposals of
Arnold G. Reinhold on http://diceware.com . It generates passphrases
by concatenating words randomly picked from wordlists. For instance::

  $ diceware
  Art83LiarRivetBlytheIs>am

The passphrase contains by default six capitalized words with no space
char or similar in-between and a single special char (the ``>`` in the
example above).

.. contents::


Install
-------

This Python package can be installed via pip_::

  $ pip install diceware

The exact way depends on your operating system.


How to Use
----------

Once installed, use ``--help`` to list all available options::

  $ diceware --help
  usage: diceware [-h] [-n NUM] [-c | --no-caps] [-s NUM]
  
  Create a passphrase
  
  optional arguments:
    -h, --help            show this help message and exit
    -n NUM, --num NUM     number of words to concatenate. Default: 6
    -c, --caps            Capitalize words. This is the default.
    --no-caps             Turn off capitalization.
    -s NUM, --specials NUM
                          Insert NUM special chars into generated word.

With ``-n`` you can tell how many words are supposed to be picked for
your new passphrase::

  $ diceware -n 1
  A*ay

  $ diceware -n 2
  FaheyFr?ed

The number of special chars put into the generated phrase can be
determined with the ``-s`` option::

  $ diceware -s 2
  LipidFool$kullRu6yI'mPack

Here ``"$"`` and ``"'"`` are the special chars.

To switch special chars completely off, set ``-s`` to zero::

  $ diceware -s 0
  LazyGainMaimBlondDentUtmost

By default the single phrase words are capitalized, i.e. the first
char of each word is made uppercase. This does not neccessarily give
better security (1 bit at most), but it helps reading a phrase.

You can nevertheless disable caps with the ``--no-caps`` option::

  $ diceware --no-caps -s 0
  oceanblendbaronferrylistenvalet

This leads to lower-case passphrases, maybe easier to type on smart
phones or similar.


What is it good for?
--------------------

Normally, `diceware` passphrases are easier to remember than shorter
passwords constructed in more or less bizarre ways. But at the same
time `diceware` passphrases provide more entropy as `xkcd`_ can show
with the famous '936' proof_:

.. image:: http://imgs.xkcd.com/comics/password_strength.png
   :align: center

.. _xkcd: http://xkcd.com/
.. _proof: http://xkcd.com/936/

The standard english wordlist of this `diceware` implementation
contains 8192 == 2**13 different english words. It is a copy of the
`Diceware8k list`_ provided by Mr. Reinhold. Therefore, picking a random word
from this list gives an entropy of 13 bits. Picking six words means an
entropy of 6 x 13 == 73 bits.

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


Credits
-------

Arnold G. Reinhold deserves all merits for the working parts of
`Diceware`_. The non-working parts are certainly my fault.

Links
-----

- Diceware_ home page
- Fork the source_ on github

Wordlists:

- `Diceware8k list`_ by Arnold G. Reinhold.


License
-------

This Python implementation of Diceware, (C) 2015 Uli Fouquet, is
licensed under the GPL v3+.

The Copyright for the Diceware_ idea and the `Diceware8k list`_ are
Copyright by Arnold G. Reinhold. See file LICENSE for details.


.. _pip: https://pip.pypa.io/en/latest/
.. _`Diceware8k list`: http://world.std.com/~reinhold/diceware8k.txt
.. _`Diceware`: http://diceware.com/
.. _`source`: http://github.com/ulif/diceware/
