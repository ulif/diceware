API
===

`diceware` code is geared towards commandline usage. You can, however,
use it from Python. The API docs are here to assist you with that.

For using `diceware` in your own, `setuptools`-based Python project,
you can add it as an install requirement in ``setup.py`` of your
project::

  from setuptools import setup
  # ...
  setup(
      name="myproject",
      # ...
      install_requires=[
          #  packages we depend on...
          'setuptools',
          'diceware',
          # ...
      ],
      # ...
  )

Of course there are other ways to make `diceware` available.


`diceware` main module
----------------------

.. automodule:: diceware
   :members:

`diceware.logger`
-----------------

.. automodule:: diceware.logger
   :members:


`diceware.config`
-----------------

.. automodule:: diceware.config
   :members:


`diceware.wordlist`
-------------------

.. automodule:: diceware.wordlist
   :members:


`diceware.random_sources`
-------------------------

.. automodule:: diceware.random_sources
   :members:
