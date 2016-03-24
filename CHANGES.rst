Changes
=======

0.6.2.dev0 (unreleased)
-----------------------

- Added sample ``.diceware.ini``.


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
