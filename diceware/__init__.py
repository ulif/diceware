#  diceware -- passphrases to remember
#  Copyright (C) 2015, 2016  Uli Fouquet
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
import pkg_resources
import sys
from random import SystemRandom
from diceware.config import get_config_dict
from diceware.wordlist import (
    WordList, get_wordlist_path, WORDLISTS_DIR, get_wordlist_names,
    )

__version__ = pkg_resources.get_distribution('diceware').version

#: Special chars inserted on demand
SPECIAL_CHARS = r"~!#$%^&*()-=+[]\{}:;" + r'"' + r"'<>?/0123456789"


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
    print("Copyright (C) 2015, 2016 Uli Fouquet")
    print("diceware is based on suggestions of Arnold G. Reinhold.")
    print("See http://diceware.com for details.")
    print("'Diceware' is a trademark of Arnold G. Reinhold.")
    print(GPL_TEXT)


def get_random_sources():
    """Get a dictionary of all entry points called diceware_random_source.

    Returns a dictionary with names mapped to callables registered as
    `entry_point`s for the ``diceware_randomsource`` group.

    Callables should accept `options` when called and return something
    that provides a `choice(sequence)` method that works like the
    respective method in the standard Python lib `random` module.
    """
    result = dict()
    for entry_point in pkg_resources.iter_entry_points(
            group="diceware_random_sources"):
        result.update({entry_point.name: entry_point.load()})
    return result


def handle_options(args):
    """Handle commandline options.
    """
    plugins = get_random_sources()
    random_sources = plugins.keys()
    wordlist_names = get_wordlist_names()
    defaults = get_config_dict()
    parser = argparse.ArgumentParser(
        description="Create a passphrase",
        epilog="Wordlists are stored in %s" % WORDLISTS_DIR
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
        '-d', '--delimiter', default='',
        help="Separate words by DELIMITER. Empty string by default.")
    parser.add_argument(
        '-r', '--randomsource', default='system', choices=random_sources,
        metavar="SOURCE",
        help=(
            "Get randomness from this source. Possible values: `%s'. "
            "Default: system" % "', `".join(sorted(random_sources))))
    parser.add_argument(
        '-w', '--wordlist', default='en_securedrop', choices=wordlist_names,
        metavar="NAME",
        help=(
            "Use words from this wordlist. Possible values: `%s'. "
            "Wordlists are stored in the folder displayed below. "
            "Default: en_securedrop" % "', `".join(wordlist_names)))
    realdice_group = parser.add_argument_group(
        "Arguments related to `realdice' randomsource",
        )
    realdice_group.add_argument(
            '--dice-sides', default=6, type=int, metavar="N",
            help='Number of sides of dice. Default: 6'
        )
    parser.add_argument(
        'infile', nargs='?', metavar='INFILE', default=None,
        type=argparse.FileType('r'),
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


def get_passphrase(options=None):
    """Get a diceware passphrase.

    `options` is a set of arguments as provided by
    `argparse.OptionParser.parse_args()`.

    The passphrase returned will contain `options.num` words deliimted by
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
    if options.infile is None:
        options.infile = open(get_wordlist_path(options.wordlist), 'r')
    word_list = WordList(options.infile)
    rnd_source = get_random_sources()[options.randomsource]
    rnd = rnd_source(options)
    words = [rnd.choice(list(word_list)) for x in range(options.num)]
    if options.caps:
        words = [x.capitalize() for x in words]
    result = options.delimiter.join(words)
    for _ in range(options.specials):
        result = insert_special_char(result, rnd=rnd)
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
    if options.version:
        print_version()
        raise SystemExit(0)
    print(get_passphrase(options))
