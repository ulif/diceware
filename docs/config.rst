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


Config Files Name and Path
--------------------------

Prior to version 1.0 we looked for a single configuration file in the calling
users' home directory only. The file had to be called::

 .diceware.ini

(please note the leading dot). If such a file were missing, buildt-in
defaults applied.

Since version 1.0 we look into several additional locations, but values set in
``.diceware.ini`` still always override settings from other configuration files
found.

In order of precedence (with highest priority first) we look into the following
paths::

    ${HOME}/.diceware.ini

Values set here override settings in any of the following files. If
``${XDG_CONFIG_HOME}`` is defined and not empty, we then look into

::

    ${XDG_CONFIG_HOME}/diceware/diceware.ini


or otherwise into

::

    ${HOME}/.config/diceware/diceware.ini

Finally, if a colon-separated and not empty list of directories is set
in

::

    ${XDG_CONFIG_DIRS}

we look up any directory in this list, appended by

::

    /diceware/diceware.ini


If none of the above files exist, default settings apply. Using this scheme we
follow the `XDG Base Directory Specification
<https://specifications.freedesktop.org/basedir-spec/latest/>`_.


Examples
........

If you set the environment variable ``${XDG_CONFIG_DIRS}`` to ``/foo:/etc``,
and then create a file ``diceware.ini`` in directory
``/foo/diceware/`` with contents like this::

    [diceware]
    num = 2

then `diceware` will create passphrases with two terms, except other
configuration files or commandline options overrule this setting.

Precedence of paths in ``${XDG_CONFIG_DIRS}`` is from least to highest
priority. Therefore, if you create a file ``/etc/diceware/diceware.ini`` with
content

::

    [diceware]
    num = 4

then this setting will override ``num = 2`` from the file above. Still any
setting in ``${XDG_CONFIG_HOME}/diceware/diceware.ini`` or
``${HOME}/.config/diceware/diceware.ini`` as explained above will take
precedence while options set in ``${HOME}/.diceware.ini`` or on the commandline
like

::

    diceware -n 6

will still have highest priority.


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
