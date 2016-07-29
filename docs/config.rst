Configuration Files
===================

You can use configuration files to persistently override built-in
defaults and make your custom settings the default.

`diceware` configuration files follow simple ``.ini``-style and look
like this::

  [diceware]
  num = 3
  caps = off
  specials = 2
  delimiter = "MYDELIMITER"
  randomsource = system
  wordlist = "en"
  dice_sides = 6

These settings would mean that by default phrases with three words
(instead six) would be created. Commandline options, however, override
config file settings. So, with the settings above::

  $ diceware
  Duma7YDELIMITER56MYDE^IMITERJock

we will get three-word phrases while with::

  $ diceware --delimiter=FOO
  AmuseFOO]us(FOO18th

we will override the config file setting for ``delimiter``. Other
settings from config file are still valid.


Option Names
------------

The options names have to match long argument names, as output with
``--help``. The values set must meet the requirements valid for
commandline usage.

You can use all or only some (or none) of the above options. Please
note that other entries, providing unknown option names, are
ignored. That means that also typos might lead to ignored entries.

Please note, that all options must be set within a section
``[diceware]``.


Config File Name and Path
-------------------------

Currently, we look for configuration files only in the calling users'
home directory. The file must be called::

 .diceware.ini

(please note the leading dot). If such a file is missing, build-in
defaults apply.


Option Values
-------------

The option values set can be strings, integers, or boolean
values.

`diceware` accepts ``yes``, ``no``, ``1``, ``0``, ``true``, ``false``,
``on``, and ``off`` as boolean values.

Some options require their setting to be taken from a fixed set of
names/values, for instance the ``randomsource`` option. You can
normally get the allowed values from calling ``diceware --help``.

String-based options (like `delimiter`) accept values enclosed in
quotes to allow whitespace-only values.

If some value cannot be parsed, an exception is raised.
