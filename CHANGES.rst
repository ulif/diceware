Changes
=======

0.9.1 (2016-12-24)
------------------

- Fixed #32, in docs tell that ``--no-caps`` option does not generate
  lower-case terms.
- Fixed #31, broken `realdice` source of randomness. `argparse` related bug,
  Bug was discovered and fixed by @LogosOfJ, thanks a lot!
- Fixed #29. Tell about code prefix problem in README.


0.9 (2016-09-14)
----------------

- Added `--dice-sides` option to tell how many sides used dices
  provide.
- Changed API interface of `get_config_dict()` to allow more flexible
  handling of config files.
- Support different verbosity levels.
- Added new wordlist ``en_eff``. It is a 7776-terms list provided by
  the Electronic Frontier Foundation. See
  https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
  for details. Thanks to `George V. Reilly
  <https://github.com/georgevreilly>`_ for hinting!
- Fixed #27. Allow dashes in numbered wordlists. Yet, these looked
  like ``1234 myterm``. We now also accept ``1-2-3-4 myterm``.


0.8 (2016-05-07)
----------------

- Closed #23. @dwcoder provided a fix that allows use of
  whitespace-only values in diceware confg files if they are enclosed
  in quotes.
- Fixed #21. @dwcoder revealed and fixed (again!). This time `--caps`
  and `--no-caps` settings did not work properly when set in CLI or in
  `.diceware.ini` config file.
- Shortened real-dice randomness source.
- Added logger as common interface to send messages to users.
- New dependency: `sphinx_rtd_theme` for generating docs. This theme
  was formerly a dependency of `Sphinx`.


0.7.1 (2016-04-21)
------------------

- Fixed #19. @dwcoder revealed and fixed a nasty bug in the real-dice
  randomness-source. Thanks a lot!


0.7 (2016-04-17)
----------------

- Added sample ``.diceware.ini``.
- Added new english wordlist ``en_securedrop``. This is the new
  default list. Thanks to `heartsucker
  <https://github.com/heartsucker>`_ who compiled and added the list.
- Remove support for Python 3.2. Several packages we depend on for testing
  and sandboxing stopped Python 3.2 support. We follow them.


0.6.1 (2015-12-15)
------------------

- Minor doc changes: add separate config file docs.
- Fix docs: the default wordlist is named ``en``. Some docs were not
  up-to-date in that regard.


0.6 (2015-12-15)
----------------

- Officially support Pyhthon 3.5.
- Tests do not depend on `pytest-cov`, `pytest-xdist` anymore.
- Support configuration files. You can set different defaults in a
  file called ``.diceware.ini`` in your home directory.
- Renamed wordlist ``en_8k`` to ``en`` as it serves as the default
  for english passphrases.


0.5 (2015-08-05)
----------------

- New option ``-r``, ``--randomsource``. We support a pluggable system
  to define alternative sources of randomness. Currently supported
  sources: ``"system"`` (to retrieve randomness from standard library,
  default) and ``realdice``, which allows use of real dice.
- New option ``-w``, ``--wordlist``. We now provide several wordlists
  for users to choose from. Own wordlists could already be fed to
  `diceware` before. By default we still use the 8192 words list from
  http://diceware.com.
- Rename `SRC_DIR` to `WORDLISTS_DIR` (reflecting what it stands for).
- Use also flake8 with tox.
- Pass `options` to `get_passphrase()` instead of a bunch of single args.
- Output wordlists dir in help output.


0.4 (2015-03-30)
----------------

- Add --delimiter option (thanks to Rodolfo Gouveia).


0.3.1 (2015-03-29)
------------------

- Turned former `diceware` module into a Python package. This is to
  fix `bug #1 Wordlists aren't included during installation
  <https://github.com/ulif/diceware/issues/1>`_, this time really.
  Wordlists will from now on be stored inside the `diceware` package.
  Again many thanks to `conorsch <https://github.com/conorsch>`_ who
  digged deep into the matter and also came up with a very considerable
  solution.
- Use readthedocs theme in docs.


0.3 (2015-03-28)
----------------

- Fix `bug #1 Wordlists aren't included during installation
  <https://github.com/ulif/diceware/issues/1>`_ . Thanks to `conorsch
  <https://github.com/conorsch>`_
- Add --version option.


0.2 (2015-03-27)
----------------

- Minor documentation changes.
- Updated copyright infos.
- Add support for custom wordlists.


0.1 (2015-02-18)
----------------

- Initial release.
