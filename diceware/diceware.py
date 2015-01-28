import os
import re
from random import SystemRandom


#: The directory in which wordlists are stored
SRC_DIR = os.path.dirname(__file__)

#: A regular expression matching ASCII chars
RE_ASCII_CHARS = re.compile('^[a-zA-Z]{2}$')

#: Special chars inserted on demand
SPECIAL_CHARS = "~!#$%^&*()-=+[]\{}:;\"'<>?/0123456789"


def get_wordlist(path):
    """Parse file at `path` and build a word list of it.

    A wordlist is expected to contain lines of format::

        <NUMS><TAB><WORD>\n

    for instance::

        136512\tTerm

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
    if not RE_ASCII_CHARS.match(lang):
        raise ValueError("Not a valid language code: %s" % lang)
    basename = 'wordlist_%s.txt' % lang
    return os.path.abspath(os.path.join(SRC_DIR, basename.lower()))


def get_passphrase(wordnum=6, specials=True, separator='', lang='en',
                   capitalized=True):
    """Get a diceware passphrase.
    """
    word_list = get_wordlist(get_wordlist_path(lang))
    rnd = SystemRandom()
    words = [rnd.choice(word_list) for x in range(wordnum)]
    if capitalized:
        words = [x.capitalize() for x in words]
    result = separator.join(words)
    result = list(result)
    result[rnd.choice(range(len(result)))] = rnd.choice(SPECIAL_CHARS)
    result = ''.join(result)
    return result


def main():
    pass
