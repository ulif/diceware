from __future__ import unicode_literals
import datetime
import os
import pytest
import re
import sys
from io import StringIO
from diceware import (
    WORDLISTS_DIR, SPECIAL_CHARS, insert_special_char, get_passphrase,
    handle_options, main, __version__, print_version, get_random_sources,
    get_wordlist_names
    )


class FakeRandom(object):
    # a very, very bad random generator.
    # Very handy for tests, though :-)

    nums_to_draw = [0] * 100

    def choice(self, elems):
        num, self.nums_to_draw = self.nums_to_draw[0], self.nums_to_draw[1:]
        return elems[num]


class TestHandleOptions(object):
    # tests for diceware.handle_options

    def test_handle_options(self):
        # we can get help
        with pytest.raises(SystemExit) as exc_info:
            handle_options(['--help'])
        assert exc_info.value.code == 0

    def test_handle_options_defaults(self):
        # defaults are correctly set
        options = handle_options([])
        assert options.num == 6
        assert options.caps is True
        assert options.specials == 0
        assert options.infile is None
        assert options.version is False
        assert options.delimiter == ""
        assert options.randomsource == "system"
        assert options.wordlist == "en_securedrop"
        assert options.verbose == 0

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

    def test_handle_options_caps(self):
        # we can set a flag to tell use of caps
        options = handle_options([])
        assert options.caps is True  # default
        options = handle_options(['-c', ])
        assert options.caps is True
        options = handle_options(['--caps', ])
        assert options.caps is True
        options = handle_options(['--no-caps', ])
        assert options.caps is False

    def test_handle_options_caps_conflicting_raises_exc(self):
        # conflicting caps-settings raise an exception
        with pytest.raises(SystemExit):
            handle_options(['--caps', '--no-caps'])
        with pytest.raises(SystemExit):
            handle_options(['--no-caps', '--caps'])

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

    def test_handle_options_verbose(self):
        # we can set verbosity level.
        options = handle_options([])
        assert options.verbose == 0
        options = handle_options(['-v', ])
        assert options.verbose == 1
        options = handle_options(['-vv', ])
        assert options.verbose == 2
        options = handle_options(['--verbose', ])
        assert options.verbose == 1
        options = handle_options(['--verbose', '--verbose', ])
        assert options.verbose == 2

    def test_handle_options_wordlist(self, capsys):
        # we can pick a wordlist
        wordlist_names = get_wordlist_names()
        for name in wordlist_names:
            options = handle_options(['-w', name])
            assert options.wordlist == name
            options = handle_options(['--wordlist', name])
            assert options.wordlist == name

    def test_handle_options_wordlist_rejects_invalid(self, capsys):
        # we can choose only existing wordlists
        with pytest.raises(SystemExit):
            handle_options(['-w', 'not-a-valid-wordlist-name'])
        out, err = capsys.readouterr()
        assert out == ''
        assert "invalid choice" in err

    def test_handle_options_dice_sides(self):
        # we can set the number of dice sides.
        options = handle_options([])
        assert options.dice_sides == 6
        options = handle_options(['--dice-sides', '21'])
        assert options.dice_sides == 21

    def test_handle_options_considers_configfile(self, home_dir):
        # defaults from a local configfile are respected
        config_file = home_dir / ".diceware.ini"
        config_file.write("\n".join(
            ["[diceware]",
             "num = 3",
             "caps = off",
             "delimiter = my-delim",
             ""]))
        options = handle_options([])
        assert options.num == 3
        assert options.delimiter == "my-delim"
        assert options.caps is False

    def test_handle_options_allows_plugins_updating(self, monkeypatch):
        # we allow plugins to update our argparser, before being used
        import diceware

        class FakePlugin(object):
            @classmethod
            def update_argparser(cls, parser):
                parser.add_argument('--foo', default=2, type=int)
                return parser

        monkeypatch.setattr(
            diceware, 'get_random_sources', lambda: dict(foo=FakePlugin))
        options = handle_options([])
        assert options.foo == 2


class TestDicewareModule(object):

    def test_get_random_sources(self):
        # we can get a dict of random sources registered as entry_points.
        sources_dict = get_random_sources()
        assert isinstance(sources_dict, dict)
        assert len(sources_dict) > 0
        assert 'system' in sources_dict
        assert isinstance(sources_dict['system'], type)

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
        options.caps = False
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
        pattern = ".*\(C\) (20[0-9]{2}, )*%s.*" % (
            datetime.datetime.now().year)
        out, err = capsys.readouterr()
        assert re.match(pattern, out, re.M + re.S) is not None

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
        out = out.replace(WORDLISTS_DIR, "<WORDLISTS-DIR>")
        out = out.replace("\n<WORDLISTS-DIR>", " <WORDLISTS-DIR>")
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

    def test_main_wordlist(self, argv_handler, capsys, wordlists_dir):
        # we can pick the wordlist we prefer
        wordlists_dir.join('wordlist_foo.txt').write("foo\n")
        wordlists_dir.join('wordlist_bar.asc').write("bar\n")
        sys.argv = ['diceware', '-w', 'foo']
        main()
        out, err = capsys.readouterr()
        assert out == 'FooFooFooFooFooFoo\n'
