import os

#: The directory in which wordlists are stored
SRC_DIR = os.path.dirname(__file__)


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


def main():
    pass
