import os
import pytest
import sys
from diceware.diceware import (
    SRC_DIR, get_wordlist, get_wordlist_path, get_passphrase, handle_options,
    main,
    )


class Test_GetWordList(object):

    def test_get_wordlist_en(self):
        # we can get a list of words out of english wordlist.
        en_src = os.path.join(SRC_DIR, 'wordlist_en.txt')
        en_result = get_wordlist(en_src)
        assert en_result[0] == 'a'
        assert en_result[-1] == '@'
        assert len(en_result) == 8192

    def test_get_wordlist_simple(self, tmpdir):
        # simple wordlists can be created
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("a\nb\n")
        assert ['a', 'b'] == get_wordlist(in_file.strpath)

    def test_get_wordlist_ignore_empty_lines(self, tmpdir):
        # we ignore empty lines in wordlists
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("\n\na\n\n")
        assert ['a'] == get_wordlist(in_file.strpath)


class TestDicewareModule(object):

    def test_get_wordlist_path(self):
        # we can get valid wordlist paths
        assert os.path.exists(get_wordlist_path('en'))
        assert not os.path.exists(get_wordlist_path('zz'))

    def test_get_wordlist_path_requires_ascii(self):
        # non ASCII alphabet chars are not accepted in language specifier
        with pytest.raises(ValueError) as exc_info:
            get_wordlist_path('../../tmp')
        assert exc_info.value.args[0].startswith(
            'Not a valid language code')

    def test_get_wordlist_path_loweres_country_code(self):
        # upper case country codes are lowered
        assert os.path.basename(get_wordlist_path('de')) == 'wordlist_de.txt'
        assert os.path.basename(get_wordlist_path('De')) == 'wordlist_de.txt'
        assert os.path.basename(get_wordlist_path('DE')) == 'wordlist_de.txt'

    def test_get_passphrase(self):
        # we can get passphrases
        r1 = get_passphrase()
        r2 = get_passphrase()
        assert r1 != r2

    def test_handle_options(self):
        # we can get help
        with pytest.raises(SystemExit) as exc_info:
            handle_options(['--help'])
        assert exc_info.value.code == 0

    def test_handle_options_defaults(self):
        # defaults are correctly set
        options = handle_options([])
        assert options.num == 6

    def test_main(self, capsys):
        # we can get help
        with pytest.raises(SystemExit) as exc_info:
            main(['diceware', '--help'])
        assert exc_info.value.code == 0
        out, err = capsys.readouterr()
        out = out.replace(
            os.path.basename(sys.argv[0]), 'diceware')
        assert out == (
            'usage: diceware [-h] [-n NUM]\n'
            '\n'
            'Create a passphrase\n'
            '\n'
            'optional arguments:\n'
            '  -h, --help         show this help message and exit\n'
            '  -n NUM, --num NUM  number of words to concatenate. Default: 6\n'
            )
