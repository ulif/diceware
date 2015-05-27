#  diceware -- passphrases to remember
#  Copyright (C) 2015  Uli Fouquet
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
import os
import pkg_resources
import re
import sys
from random import SystemRandom

__version__ = pkg_resources.get_distribution('diceware').version

#: The directory in which wordlists are stored
WORDLISTS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'wordlists'))

#: A regular expression matching 2 consecutive ASCII chars. We
#: consider this to represent some language/country code.
RE_LANG_CODE = re.compile('^[a-zA-Z]{2}$')

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
    print("Copyright (C) 2015 Uli Fouquet")
    print("diceware is based on suggestions of Arnold G. Reinhold.")
    print("See http://diceware.com for details.")

    print("'Diceware' is a trademark of Arnold G. Reinhold.")
    print(GPL_TEXT)


def handle_options(args):
    """Handle commandline options.
    """
    parser = argparse.ArgumentParser(description="Create a passphrase")
    parser.add_argument(
        '-n', '--num', default=6, type=int,
        help='number of words to concatenate. Default: 6')
    cap_group = parser.add_mutually_exclusive_group()
    cap_group.add_argument(
        '-c', '--caps', action='store_true',
        help='Capitalize words. This is the default.')
    cap_group.add_argument(
        '--no-caps', action='store_false', dest='capitalize',
        help='Turn off capitalization.')
    parser.add_argument(
        '-s', '--specials', default=0, type=int, metavar='NUM',
        help="Insert NUM special chars into generated word.")
    parser.add_argument(
        '-d', '--delimiter', default='',
        help="Separate words by DELIMITER. Empty string by default.")
    parser.add_argument(
        '-i', '--input-dice-results', action='store_true',
        help="Input dice results instead of choosing randomly (ignore \"-n\").")
    parser.add_argument(
        'infile', nargs='?', metavar='INFILE', default=None,
        type=argparse.FileType('r'),
        help="Input wordlist. `-' will read from stdin.",
        )
    parser.add_argument(
        '--version', action='store_true',
        help='output version information and exit.',
        )
    parser.set_defaults(capitalize=True)
    args = parser.parse_args(args)
    return args


def get_wordlist(file_descriptor):
    """Parse file in `file_descriptor` and build a word list of it.

    `file_descriptor` is expected to be a file descriptor, already
    opened for reading. The descriptor will be closed after
    processing.

    A wordlist is expected to contain lines of words. Each line a
    word. Empty lines are ignored. Returns a list of terms (lines)
    found.
    """
    result = [
        line.strip() for line in file_descriptor.readlines()
        if line.strip() != '']
    file_descriptor.close()
    return result


def get_wordlist_path(lang):
    """Get path to a wordlist file for language `lang`.

    The `lang` string is a 2-char country code. Invalid codes raise a
    ValueError.
    """
    if not RE_LANG_CODE.match(lang):
        raise ValueError("Not a valid language code: %s" % lang)
    basename = 'wordlist_%s.txt' % lang
    return os.path.join(WORDLISTS_DIR, basename.lower())


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


def get_words_from_dice_results(wordlist):
    """Get a list of words based on the results of real dice throws.
    """
    words = []
    num = 1
    error_msg = "Error: input must be exactly 5 numbers between 1 and 6."
    print("Input 5 dice results per line, finish with an empty line.")
    while True:
        error = False
        dice_results = raw_input("  Word #%d: " % num)
        if dice_results == '':
            # finished inputting words!
            break
        # validate input length
        if len(dice_results) != 5:
            print(error_msg)
            error = True
        # validate input values
        for c in dice_results:
            if c not in ['1', '2', '3', '4', '5', '6']:
                print(error_msg)
                error = True
                break
        if error:
            continue
        index = get_word_index_from_input(dice_results)
        words.append(wordlist[index])
        num += 1
    return words


def get_word_index_from_input(dice_results):
    """Calculate a decimal index based on the dice results.
    """
    coefficients = [ord(c) - 49 for c in dice_results]  # '1' is 49 in ascii
    coefficients.reverse()
    # calculate the result of the base 6 polynomial with coefficients given by
    # the dice throw results
    result = 0
    power = 0
    for c in coefficients:
        result += c * (6 ** power)
        power += 1
    return result


def get_passphrase(wordnum=6, specialsnum=1, delimiter='', lang='en',
                   capitalized=True, wordlist_fd=None,
                   input_dice_results=False):
    """Get a diceware passphrase.

    The passphrase returned will contain `wordnum` words deliimted by
    `delimiter`.

    If `capitalized` is ``True``, all words will be capitalized.

    If `wordlist_fd`, a file descriptor, is given, it will be used
    instead of a 'built-in' wordlist (and `lang` will be
    ignored). `wordlist_fd` must be open for reading.

    The wordlist to pick words from is determined by `lang`,
    representing a language (unless `wordlist_fd` is given).

    """
    if wordlist_fd is None:
        wordlist_fd = open(get_wordlist_path(lang), 'r')
    word_list = get_wordlist(wordlist_fd)
    if not input_dice_results:
        rnd = SystemRandom()
        words = [rnd.choice(word_list) for x in range(wordnum)]
    else:
        words = get_words_from_dice_results(word_list)
    if capitalized:
        words = [x.capitalize() for x in words]
    result = delimiter.join(words)
    for _ in range(specialsnum):
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
    print(
        get_passphrase(
            wordnum=options.num,
            specialsnum=options.specials,
            delimiter=options.delimiter,
            capitalized=options.capitalize,
            wordlist_fd=options.infile,
            input_dice_results=options.input_dice_results,
        )
    )
