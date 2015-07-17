from __future__ import unicode_literals
import datetime
import os
import pytest
import sys
from io import StringIO
from diceware import (
    WORDLISTS_DIR, RE_WORDLIST_NAME, SPECIAL_CHARS, get_wordlist,
    get_wordlist_path, insert_special_char, get_passphrase,
    handle_options, main, __version__, print_version, get_random_sources,
    get_wordlist_names,
    )


class FakeRandom(object):
    # a very, very bad random generator.
    # Very handy for tests, though :-)

    nums_to_draw = [0] * 100

    def choice(self, elems):
        num, self.nums_to_draw = self.nums_to_draw[0], self.nums_to_draw[1:]
        return elems[num]


@pytest.fixture(scope="function")
def argv_handler(request):
    """This fixture restores sys.argv and sys.stdin after tests.
    """
    _argv_stored = sys.argv
    _stdin_stored = sys.stdin

    def teardown():
        sys.argv = _argv_stored
        sys.stdin = _stdin_stored
    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def wordlists_dir(request, monkeypatch, tmpdir):
    """This fixture provides a temporary wordlist dir.
    """
    monkeypatch.setattr("diceware.WORDLISTS_DIR", str(tmpdir))
    return tmpdir


class Test_GetWordList(object):

    def test_get_wordlist_en_8k(self):
        # we can get a list of words out of english 8k wordlist.
        en_src = os.path.join(WORDLISTS_DIR, 'wordlist_en_8k.txt')
        with open(en_src, 'r') as fd:
            en_result = get_wordlist(fd)
        assert en_result[0] == 'a'
        assert en_result[-1] == '@'
        assert len(en_result) == 8192

    def test_get_wordlist_simple(self, tmpdir):
        # simple wordlists can be created
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("a\nb\n")
        with open(in_file.strpath, 'r') as fd:
            result = get_wordlist(fd)
        assert ['a', 'b'] == result

    def test_get_wordlist_ignore_empty_lines(self, tmpdir):
        # we ignore empty lines in wordlists
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("\n\na\n\n")
        with open(in_file.strpath, 'r') as fd:
            result = get_wordlist(fd)
        assert ['a'] == result

    def test_get_wordlist_closes_fd(self, tmpdir):
        # we close passed-in file descriptors
        in_file = tmpdir.join("somewordlist")
        in_file.write("aaa\nbbb\n")
        with open(in_file.strpath, 'r') as fd:
            get_wordlist(fd)
            assert fd.closed is True


class TestDicewareModule(object):

    def test_re_wordlist_name(self):
        # RE_WORDLIST_NAME really works
        # valid stuff
        assert RE_WORDLIST_NAME.match('de') is not None
        assert RE_WORDLIST_NAME.match('DE') is not None
        assert RE_WORDLIST_NAME.match('vb') is not None
        assert RE_WORDLIST_NAME.match('8k') is not None
        assert RE_WORDLIST_NAME.match('original') is not None
        assert RE_WORDLIST_NAME.match('with_underscore') is not None
        assert RE_WORDLIST_NAME.match('u') is not None
        assert RE_WORDLIST_NAME.match('with-hyphen') is not None
        # invalid stuff
        assert RE_WORDLIST_NAME.match('with space') is None
        assert RE_WORDLIST_NAME.match('"with-quotation-marks"') is None
        assert RE_WORDLIST_NAME.match("'with-quotation-marks'") is None
        assert RE_WORDLIST_NAME.match('with.dot') is None
        assert RE_WORDLIST_NAME.match('with/slash') is None

    def test_get_random_sources(self):
        # we can get a dict of random sources registered as entry_points.
        sources_dict = get_random_sources()
        assert isinstance(sources_dict, dict)
        assert len(sources_dict) > 0
        assert 'system' in sources_dict
        assert isinstance(sources_dict['system'], type)

    def test_get_wordlist_path(self):
        # we can get valid wordlist paths
        assert os.path.exists(get_wordlist_path('en_8k'))
        assert not os.path.exists(get_wordlist_path('zz'))

    def test_get_wordlist_path_requires_ascii(self):
        # non ASCII alphabet chars are not accepted in language specifier
        with pytest.raises(ValueError) as exc_info:
            get_wordlist_path('../../tmp')
        assert exc_info.value.args[0].startswith(
            'Not a valid wordlist name')

    def test_get_wordlist_names(self, wordlists_dir):
        # we can get wordlist names also if directory is empty.
        wlist_path = wordlists_dir.join('mywordlist_en_8k.txt')
        wlist_path.write("some\nirrelevant\nwords")
        assert get_wordlist_names() == ['en_8k']

    def test_insert_special_char(self):
        # we can insert special chars in words.
        fake_rnd = FakeRandom()
        result1 = insert_special_char('foo', specials='bar', rnd=fake_rnd)
        assert result1 == 'boo'
        fake_rnd.nums_to_draw = [1, 1]
        result2 = insert_special_char('foo', specials='bar', rnd=fake_rnd)
        assert result2 == 'fao'
        fake_rnd.nums_to_draw = [2, 2]
        result3 = insert_special_char('foo', specials='bar', rnd=fake_rnd)
        assert result3 == 'for'
        fake_rnd.nums_to_draw = [0, 0]
        result4 = insert_special_char('foo', rnd=fake_rnd)
        assert result4 == '~oo'

    def test_insert_special_char_defaults(self):
        # defaults are respected
        expected_matrix = []
        for i in range(3):
            for j in range(len(SPECIAL_CHARS)):
                word = list('foo')
                word[i] = SPECIAL_CHARS[j]
                expected_matrix.append(''.join(word))
        for x in range(100):
            assert insert_special_char('foo') in expected_matrix

    def test_special_chars_do_not_quote(self):
        # backslashes in SPECIAL_CHAR do not hide away chars
        assert len(SPECIAL_CHARS) == 36

    def test_get_passphrase(self):
        # we can get passphrases
        r1 = get_passphrase()
        r2 = get_passphrase()
        assert r1 != r2

    def test_get_passphrase_capitals(self):
        # by default a passphrase contains upper case chars
        phrase = get_passphrase()
        assert phrase.lower() != phrase

    def test_get_passphrase_no_capitals(self):
        # we can turn capitals off
        options = handle_options(args=[])
        options.capitalize = False
        phrase = get_passphrase(options)
        assert phrase.lower() == phrase

    def test_get_passphrase_specialchars(self):
        # we can request special chars in passphrases
        options = handle_options(args=[])
        options.specials = 2
        phrase = get_passphrase(options)
        specials = [x for x in phrase if x in SPECIAL_CHARS]
        # the 2nd special char position might be equal to 1st.
        assert len(specials) > 0

    def test_get_passphrase_delimiters(self):
        # we can set separators
        options = handle_options(args=[])
        options.delimiter = " "
        phrase = get_passphrase(options)
        assert " " in phrase

    def test_get_passphrase_wordlist_fd(self):
        #  we can pass in an own wordlist
        options = handle_options(args=[])
        options.infile = StringIO("word1\n")
        phrase = get_passphrase(options)
        assert "Word1" in phrase

    def test_print_version(self, capsys):
        # we can print version infos
        print_version()
        out, err = capsys.readouterr()
        assert err == ''
        assert __version__ in out

    def test_print_version_current_year(self, capsys):
        # in version infos we display the current year
        print_version()
        expected = '(C) %s' % (datetime.datetime.now().year)
        out, err = capsys.readouterr()
        assert expected in out

    def test_handle_options(self):
        # we can get help
        with pytest.raises(SystemExit) as exc_info:
            handle_options(['--help'])
        assert exc_info.value.code == 0

    def test_handle_options_defaults(self):
        # defaults are correctly set
        options = handle_options([])
        assert options.num == 6
        assert options.capitalize is True
        assert options.specials == 0
        assert options.infile is None
        assert options.version is False
        assert options.delimiter == ""
        assert options.randomsource == "system"

    def test_handle_options_infile(self, tmpdir):
        # we can give an infile
        tmpdir.chdir()
        with open('mywords', 'w') as fd:
            fd.write('one\ntwo\n')
        options = handle_options(['mywords', ])
        assert options.infile is not None
        assert options.infile.read() == 'one\ntwo\n'

    def test_handle_options_version(self):
        # we can ask for version infos
        options = handle_options(['--version', ])
        assert options.version is True

    def test_handle_options_delimiter(self):
        # we can set delimiter
        options = handle_options(['-d', ' '])
        assert options.delimiter == ' '
        options = handle_options(['--delimiter', ' '])
        assert options.delimiter == ' '
        options = handle_options(['-d', 'WOW'])
        assert options.delimiter == 'WOW'

    def test_handle_options_randomsource(self):
        # we can choose the source of randomness
        source_names = get_random_sources().keys()
        for name in source_names:
            options = handle_options(['-r', name])
            assert options.randomsource == name
            options = handle_options(['--randomsource', name])
            assert options.randomsource == name

    def test_handle_options_randomsource_rejects_invalid(self, capsys):
        # we can not choose illegal values for source of randomness
        with pytest.raises(SystemExit):
            handle_options(['-r', 'not-a-valid-source-name'])
        out, err = capsys.readouterr()
        assert out == ''
        assert "invalid choice" in err

    def test_main(self, capsys):
        # we can get a passphrase
        main([])  # call with default options in place
        out, err = capsys.readouterr()
        assert err == ''               # we got no errors
        assert out[-1] == '\n'         # output ends with liebreak
        assert not ('\n' in out[:-1])  # we get one line
        assert len(out) > 5            # we get at least some chars

    def test_main_help(self, argv_handler, capsys):
        # we can get help
        sys.argv = ['diceware', '--help']
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        out, err = capsys.readouterr()
        expected_path = os.path.join(
            os.path.dirname(__file__), 'exp_help_output.txt')
        with open(expected_path, 'r') as fd:
            expected_output = fd.read()
        assert out == expected_output

    def test_main_version(self, argv_handler, capsys):
        # we can get version infos.
        sys.argv = ['diceware', '--version']
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        out, err = capsys.readouterr()
        assert __version__ in out

    def test_main_argv(self, argv_handler):
        # main() handles sys.argv if nothing is provided
        sys.argv = ['diceware', '--help']
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_main_infile(self, argv_handler, tmpdir, capsys):
        # main() reads custom wordlist if provided
        custom_path = tmpdir.join('mywordlist.txt')
        custom_path.write('mysingleword\n')
        tmpdir.chdir()
        main(['-n', '1', 'mywordlist.txt', ])
        out, err = capsys.readouterr()
        assert out == 'Mysingleword\n'

    def test_main_infile_stdin(self, argv_handler, capsys):
        # main() also accepts input from stdin
        sys.stdin = StringIO("word1\n")
        sys.argv = ['diceware', '-n', '2', '-']
        main()
        out, err = capsys.readouterr()
        assert out == 'Word1Word1\n'

    def test_main_delimiters(self, argv_handler, capsys):
        # delimiters are respected on calls to main
        sys.stdin = StringIO("word1\n")
        sys.argv = ['diceware', '-n', '2', '-d', 'DELIM', '-']
        main()
        out, err = capsys.readouterr()
        assert out == 'Word1DELIMWord1\n'

    def test_main_specialchars(self, argv_handler, capsys):
        # number of specialchars is respected in calls to main.
        sys.stdin = StringIO("word1\n")
        sys.argv = ['diceware', '-n', '1', '-s', '1', '-']
        main()
        out, err = capsys.readouterr()
        specials = [x for x in out if x in SPECIAL_CHARS]
        assert len(specials) > 0
