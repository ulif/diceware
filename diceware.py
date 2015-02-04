import argparse
import os
import re
import sys
from random import SystemRandom


#: The directory in which wordlists are stored
SRC_DIR = os.path.dirname(__file__)

#: A regular expression matching 2 consecutive ASCII chars. We
#: consider this to represent some language/country code.
RE_LANG_CODE = re.compile('^[a-zA-Z]{2}$')

#: Special chars inserted on demand
SPECIAL_CHARS = "~!#$%^&*()-=+[]\{}:;\"'<>?/0123456789"


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
    parser.set_defaults(capitalize=True)
    args = parser.parse_args(args)
    return args


def get_wordlist(path):
    """Parse file at `path` and build a word list of it.

    A wordlist is expected to contain lines of words. Each line a
    word. Empty lines are ignored. Returns a list of terms (lines)
    found.
    """
    result = []
    with open(path, 'r') as fd:
        result = [line.strip() for line in fd.readlines()
                  if line.strip() != '']
    return result


def get_wordlist_path(lang):
    """Get path to a wordlist file for language `lang`.

    The `lang` string is a 2-char country code. Invalid codes raise a
    ValueError.
    """
    if not RE_LANG_CODE.match(lang):
        raise ValueError("Not a valid language code: %s" % lang)
    basename = 'wordlist_%s.txt' % lang
    return os.path.abspath(os.path.join(
        SRC_DIR, 'wordlists', basename.lower()))


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


def get_passphrase(wordnum=6, specialsnum=1, delimiter='', lang='en',
                   capitalized=True):
    """Get a diceware passphrase.

    The passphrase returned will contain `wordnum` words deliimted by
    `delimiter`.

    If `capitalized` is ``True``, all words will be capitalized.

    The wordlist to pick words from is determined by `lang`,
    representing a language.
    """
    word_list = get_wordlist(get_wordlist_path(lang))
    rnd = SystemRandom()
    words = [rnd.choice(word_list) for x in range(wordnum)]
    if capitalized:
        words = [x.capitalize() for x in words]
    result = delimiter.join(words)
    for x in range(specialsnum):
        result = insert_special_char(result, rnd=rnd)
    return result


def main(args=1):
    if args is 1:
        args = sys.argv[1:]
    options = handle_options(args)
    print(get_passphrase(
        wordnum=options.num,
        specialsnum=options.specials,
        capitalized=options.capitalize
        )
    )
