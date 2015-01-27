import os
import re

#: The directory in which wordlists are stored
SRC_DIR = os.path.dirname(__file__)

#: A regular expression matching ASCII chars
RE_ASCII_CHARS = re.compile('^[a-zA-Z]{2}$')


def get_wordlist(path):
    """Parse file at `path` and build a word list of it.

    A wordlist is expected to contain lines of format::

        <NUMS><TAB><WORD>\n

    for instance::

        136512\tTerm

    """
    result = []
    with open(path, 'r') as fd:
        for line in fd.readlines():
            if not '\t' in line:
                continue
            term = line.split('\t')[1].strip()
            if term != '':  # do not accept empty strings
                result.append(term)
    return result


def get_wordlist_path(lang):
    """Get path to a wordlist file for language `lang`.

    The `lang` string is a 2-char country code. Invalid codes raise a
    ValueError.
    """
    basename = 'wordlist_%s.asc' % lang
    if not RE_ASCII_CHARS.match(lang):
        raise ValueError("Not a valid language code: %s" % lang)
    return os.path.abspath(os.path.join(SRC_DIR, basename.lower()))


def main():
    pass
