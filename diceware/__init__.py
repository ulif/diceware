#  diceware -- passphrases to remember
#  Copyright (C) 2015-2022  Uli Fouquet
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""diceware -- rememberable passphrases
"""
import argparse
import sys
import logging
from errno import ENOENT
from random import SystemRandom
from .__about__ import version as __version__
from diceware.config import get_config_dict
from diceware.logger import configure
from diceware.wordlist import (
    WordList, get_wordlist_path, get_wordlists_dir, get_wordlist_names,
    )

#: Special chars inserted on demand
SPECIAL_CHARS = r"~!#$%^&*()-=+[]\{}:;" + r'"' + r"'<>?/"
DIGIT_CHARS = r"0123456789"

GPL_TEXT = (
    """
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """
    )


def print_version():
    """Output current version and other infos.
    """
    print("diceware %s" % __version__)
    print("Copyright (C) 2015-2024 Uli Fouquet")
    print("diceware is based on suggestions of Arnold G. Reinhold.")
    print("See http://diceware.com for details.")
    print("'Diceware' is a trademark of Arnold G Reinhold,"
          " used with permission")
    print(GPL_TEXT)


def get_random_sources():
    """Get a dictionary of all entry points called diceware_random_source.

    Returns a dictionary with names mapped to callables registered as
    `entry_point`s for the ``diceware_randomsource`` group.

    Callables should accept `options` when called and return something
    that provides a `choice(sequence)` method that works like the
    respective method in the standard Python lib `random` module.
    """
    from .__about__ import random_sources
    result = dict()
    for name, spec in random_sources.items():
        module, func = spec.split(":")
        module = __import__(module, fromlist=['__name__'], level=0)
        try:
            func = getattr(module, func)
        except AttributeError as exc:
            raise ImportError(str(exc))
        result[name] = func
    return result


def handle_options(args):
    """Handle commandline options.
    """
    plugins = get_random_sources()
    rnd_sources = plugins.keys()
    wordlist_names = get_wordlist_names()
    defaults = get_config_dict()
    parser = argparse.ArgumentParser(
        description="Create a passphrase",
        epilog="Wordlists are stored in %s" % get_wordlists_dir()
        )
    parser.add_argument(
        '-n', '--num', default=6, type=int,
        help='number of words to concatenate. Default: 6')
    cap_group = parser.add_mutually_exclusive_group()
    cap_group.add_argument(
        '-c', '--caps', action='store_true',
        help='Capitalize words. This is the default.')
    cap_group.add_argument(
        '--no-caps', action='store_false', dest='caps',
        help='Turn off capitalization.')
    parser.add_argument(
        '-s', '--specials', default=0, type=int, metavar='NUM',
        help="Insert NUM special chars into generated word.")
    parser.add_argument(
        '-D', '--digits', default=0, type=int, metavar='NUM',
        help="Insert NUM digit chars into generated word.")
    parser.add_argument(
        '-d', '--delimiter', default='',
        help="Separate words by DELIMITER. Empty string by default.")
    parser.add_argument(
        '-r', '--randomsource', default='system', choices=rnd_sources,
        metavar="SOURCE",
        help=(
            "Get randomness from this source. Possible values: `%s'. "
            "Default: system" % "', `".join(sorted(rnd_sources))))
    parser.add_argument(
        '-w', '--wordlist', default=['en_eff'], choices=wordlist_names,
        metavar="NAME", nargs='*',
        help=(
            "Use words from this wordlist. Possible values: `%s'. "
            "Wordlists are stored in the folder displayed below. "
            "Default: en_eff" % "', `".join(wordlist_names)))
    realdice_group = parser.add_argument_group(
        "Arguments related to `realdice' randomsource",
        )
    realdice_group.add_argument(
            '--dice-sides', default=6, type=int, metavar="N",
            help='Number of sides of dice. Default: 6'
        )
    parser.add_argument(
        'infile', nargs='?', metavar='INFILE', default=None,
        help="Input wordlist. `-' will read from stdin.",
        )
    parser.add_argument(
        '-v', '--verbose', action='count',
        help='Be verbose. Use several times for increased verbosity.')
    parser.add_argument(
        '--version', action='store_true',
        help='output version information and exit.',
        )
    for plugin in plugins.values():
        if hasattr(plugin, "update_argparser"):
            parser = plugin.update_argparser(parser)
    parser.set_defaults(**defaults)
    args = parser.parse_args(args)
    return args


def insert_special_char(word, specials=SPECIAL_CHARS, rnd=None):
    """Insert a char out of `specials` into `word`.

    `rnd`, if passed in, will be used as a (pseudo) random number
    generator. We use `.choice()` only.

    Returns the modified word.
    """
    if rnd is None:
        rnd = SystemRandom()
    char_list = list(word)
    char_list[rnd.choice(range(len(char_list)))] = rnd.choice(specials)
    return ''.join(char_list)


def insert_digit_char(word, digits=DIGIT_CHARS, rnd=None):
    """Insert a char out of `digits` into `word`.

    `rnd`, if passed in, will be used as a (pseudo) random number
    generator. We use `.choice()` only.

    Returns the modified word.
    """
    if rnd is None:
        rnd = SystemRandom()
    char_list = list(word)
    char_list[rnd.choice(range(len(char_list)))] = rnd.choice(digits)
    return ''.join(char_list)


def get_passphrase(options=None):
    """Get a diceware passphrase.

    `options` is a set of arguments as provided by
    `argparse.OptionParser.parse_args()`.

    The passphrase returned will contain `options.num` words delimited by
    `options.delimiter` and `options.specials` special chars.

    For the passphrase generation we will use the random source
    registered under the name `options.randomsource` (something like
    "system" or "dice").

    If `options.caps` is ``True``, all words will be caps.

    If `options.infile`, a file descriptor, is given, it will be used
    instead of a 'built-in' wordlist. `options.infile` must be open for
    reading.
    """
    if options is None:
        options = handle_options(args=[])
    rnd_source = get_random_sources()[options.randomsource]
    rnd = rnd_source(options)

    words = []
    paths = [options.infile]
    if paths == [None]:
        paths = [get_wordlist_path(x) for x in options.wordlist]
    wordlists = [list(WordList(path)) for path in paths]
    for x_ in range(options.num):
        for wordlist in wordlists:
            words.append(rnd.choice(wordlist))
    if options.caps:
        words = [x.capitalize() for x in words]
    result = options.delimiter.join(words)
    for _ in range(options.specials):
        result = insert_special_char(result, rnd=rnd)
    for _ in range(options.digits):
        result = insert_digit_char(result, rnd=rnd)
    return result


def main(args=None):
    """Main programme.

    Called when `diceware` script is called.

    `args` is a list of command line arguments to process. If no such
    args are given, we use `sys.argv`.
    """
    if args is None:
        args = sys.argv[1:]
    options = handle_options(args)
    configure(options.verbose)
    if options.version:
        print_version()
        raise SystemExit(0)
    try:
        print(get_passphrase(options))
    except (OSError, IOError) as infile_error:
        if getattr(infile_error, 'errno', 0) == ENOENT:
            logging.getLogger('ulif.diceware').error(
                "The file '%s' does not exist." % infile_error.filename)
            raise SystemExit(1)
        else:
            raise
