import os
from diceware.diceware import SRC_DIR, get_wordlist


def test_get_wordlist_en():
    # we can get a list of words out of english wordlist.
    en_src = os.path.join(SRC_DIR, 'wordlist_en.asc')
    en_result = get_wordlist(en_src)
    assert en_result[0] == 'a'
    assert en_result[-1] == '@'
    assert len(en_result) == 7776
