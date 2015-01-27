import os
from diceware.diceware import SRC_DIR, get_wordlist


class Test_GetWordList(object):

    def test_get_wordlist_en(self):
        # we can get a list of words out of english wordlist.
        en_src = os.path.join(SRC_DIR, 'wordlist_en.asc')
        en_result = get_wordlist(en_src)
        assert en_result[0] == 'a'
        assert en_result[-1] == '@'
        assert len(en_result) == 7776

    def test_get_wordlist_simple(self, tmpdir):
        # simple wordlists can be created
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("01\ta\n02\tb\n")
        assert ['a', 'b'] == get_wordlist(in_file.strpath)

    def test_get_wordlist_ignore_empty_lines(self, tmpdir):
        # we ignore empty lines in wordlists
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("\n\n\n")
        assert [] == get_wordlist(in_file.strpath)

    def test_get_wordlist_ignore_non_data(self, tmpdir):
        # lines without tabs ('\t') are ignored
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("111111  a\n111112  b\n")
        assert [] == get_wordlist(in_file.strpath)

    def test_get_wordlist_broken(self, tmpdir):
        # we handle broken lines gracefully
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("11\ta\t12\n22\t\n\n33\tc")
        assert ['a', 'c'] == get_wordlist(in_file.strpath)
