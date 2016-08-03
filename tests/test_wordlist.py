import os
import pytest
from io import StringIO
from diceware.wordlist import (
    WORDLISTS_DIR, RE_WORDLIST_NAME, RE_NUMBERED_WORDLIST_ENTRY,
    RE_VALID_WORDLIST_FILENAME, get_wordlist_path, get_wordlist_names,
    WordList,
)


@pytest.fixture(scope="function")
def wordlist(request, tmpdir):
    """A fixture that delivers a simple WordList instance.
    """
    path = tmpdir.join("mylist.txt")
    path.write("foo\nbar\n")
    w_list = WordList(str(path))
    return w_list


class TestWordlistModule(object):

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

    def test_re_numbered_wordlist_entry(self):
        # we accept numbers (optionally separated by single dashes) in
        # wordlist lines
        #
        # valid stuff
        assert RE_NUMBERED_WORDLIST_ENTRY.match('11111   a') is not None
        assert RE_NUMBERED_WORDLIST_ENTRY.match('1-2-2-11 1') is not None
        assert RE_NUMBERED_WORDLIST_ENTRY.match(
            '11111   a').groups() == (None, 'a', )
        assert RE_NUMBERED_WORDLIST_ENTRY.match('12211\t 1') is not None
        assert RE_NUMBERED_WORDLIST_ENTRY.match(
            '12211\t 1').groups() == (None, '1', )
        assert RE_NUMBERED_WORDLIST_ENTRY.match(
            '1-2-2-1-1\t 1-1').groups()[1] == '1-1'
        # invalid stuff
        assert RE_NUMBERED_WORDLIST_ENTRY.match('12a11 foo') is None
        assert RE_NUMBERED_WORDLIST_ENTRY.match('12--11 foo') is None
        assert RE_NUMBERED_WORDLIST_ENTRY.match('1211- foo') is None
        assert RE_NUMBERED_WORDLIST_ENTRY.match('-1211 foo') is None
        assert RE_NUMBERED_WORDLIST_ENTRY.match('foo bar') is None

    def test_re_valid_wordlist_filename(self):
        # RE_VALID_WORDLIST_FILENAME really detects filenames we allow
        # Valid filenames
        regexp = RE_VALID_WORDLIST_FILENAME
        assert regexp.match("wordlist_foo.txt") is not None
        assert regexp.match("wordlist_foo_bar.asc") is not None
        assert regexp.match("wordlist_name-withdots.txt.asc") is not None
        assert regexp.match("wordlist_en.txt") is not None
        assert regexp.match("wordlist_en_eff.txt") is not None
        assert regexp.match("wordlist_en_orig.asc") is not None
        assert regexp.match("wordlist_en_securedrop.asc") is not None
        # We can get the internal wordlist name
        assert regexp.match("wordlist_foo.txt").groups()[0] == "foo"
        assert regexp.match(
            "wordlist_foo_bar.asc").groups()[0] == "foo_bar"
        assert regexp.match(
            "wordlist_name-with.dots.txt.asc").groups()[0] == "name-with"
        # Invalid names
        assert regexp.match("wordlist-without-underscore.txt") is None
        assert regexp.match("wordlist_invalid_ch=r.txt") is None
        assert regexp.match("wordlist_without_dot_txt") is None
        assert regexp.match("nowordlist_foo.txt") is None
        assert regexp.match("wordlist_name.") is None
        assert regexp.match("wordlist_name.txt.") is None
        assert regexp.match("wordlist_name.txt..") is None
        assert regexp.match("wordlist_name.txt/..") is None
        assert regexp.match("wordlist_.txt") is None

    def test_get_wordlist_path(self, wordlists_dir):
        # we can get valid wordlist paths
        path1 = wordlists_dir.join("wordlist_foo.txt")
        path1.write("foo\n")
        path2 = wordlists_dir.join("wordlist_bar.asc")
        path2.write("bar\n")
        assert get_wordlist_path('foo') == path1
        assert get_wordlist_path('bar') == path2
        assert get_wordlist_path('zz') is None

    def test_get_wordlist_path_ignores_subdirs(self, wordlists_dir):
        # we subdirs are ignored, when looking for wordlists.
        path1 = wordlists_dir.mkdir('wordlist_subdir1.txt')
        path2 = wordlists_dir.join('wordlist_subdir2.txt')
        path2.write('foo\n')
        assert os.path.isdir(str(path1))
        assert os.path.isfile(str(path2))
        assert get_wordlist_path('subdir1') is None
        assert get_wordlist_path('subdir2') == str(path2)

    def test_get_wordlist_path_accepts_any_ext(self, wordlists_dir):
        # we cope with any filename extension, not only .txt
        path1 = wordlists_dir.join("wordlist_foo.txt")
        path1.write("foo\n")
        path2 = wordlists_dir.join("wordlist_bar.asc")
        path2.write("bar\n")
        path3 = wordlists_dir.join("wordlist_baz.txt.asc")
        path3.write("baz\n")
        assert get_wordlist_path("foo") == str(path1)
        assert get_wordlist_path("bar") == str(path2)
        assert get_wordlist_path("baz") == str(path3)
        assert get_wordlist_path("not-existing") is None

    def test_get_wordlist_path_requires_ascii(self):
        # non ASCII alphabet chars are not accepted in language specifier
        with pytest.raises(ValueError) as exc_info:
            get_wordlist_path('../../tmp')
        assert exc_info.value.args[0].startswith(
            'Not a valid wordlist name')

    def test_get_wordlist_names(self, wordlists_dir):
        # we can get wordlist names also if directory is empty.
        wlist_path = wordlists_dir.join('wordlist_my_en.txt')
        wlist_path.write("some\nirrelevant\nwords")
        assert get_wordlist_names() == ['my_en']

    def test_get_wordlist_names_files_only(self, wordlists_dir):
        # non-files are ignored when looking for wordlist names
        sub_dir = wordlists_dir.mkdir('subdir')                # a subdir
        sub_dir.join("somfile_name.txt").write("Some\ntext")   # and a file in
        assert get_wordlist_names() == []

    def test_get_wordlist_names_requires_underscore(self, wordlists_dir):
        # we only recognize wordlist files with underscore in name
        wordlists_dir.join("file-without-underscore.txt").write("a\nb\n")
        assert get_wordlist_names() == []

    def test_get_wordlist_names_requires_dot(self, wordlists_dir):
        # we only recognize wordlist files with dot in name
        wordlists_dir.join("file_without_dot-in-name").write("a\nb\n")
        assert get_wordlist_names() == []


class TestWordList(object):

    def test_create_wordlist(self, tmpdir):
        # we can create `WordList` objects.
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("foo\n")
        w_list = WordList(str(in_file))
        assert w_list is not None
        assert hasattr(w_list, "path")
        assert hasattr(w_list, "fd")
        assert hasattr(w_list, "signed")

    def test_create_opens_file(self, tmpdir):
        # if we pass-in a path, the file will be opened for reading.
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("foo\n")
        w_list = WordList(str(in_file))
        assert w_list.fd is not None

    def test_create_accepts_open_file(self, tmpdir):
        # if we pass in an open file, it will be used
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("foo\n")
        with open(str(in_file), "r") as my_open_file:
            w_list = WordList(my_open_file)
            assert w_list.fd is not None
            assert w_list.path is None

    def test_create_accepts_fd_with_broken_seek(self, argv_handler):
        # we accept files that have no working seek() (like sys.stdin)
        fd = StringIO(b"word1\nword2\n".decode("utf-8"))

        def broken_seek(num):
            raise IOError("Illegal seek")
        fd.seek = broken_seek
        w_list = WordList(fd)
        assert w_list.fd is not fd

    def test_open_file_descriptor_simple(self, tmpdir):
        # we handle simple lists from open file descriptors correctly
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("foo\nbar\n\nbaz\n")
        with open(str(in_file), "r") as my_open_file:
            w_list = WordList(my_open_file)
            result = tuple(w_list)
        assert result == ("foo", "bar", "baz")

    def test_open_file_descriptor_signed(self):
        # we can handle signed wordlists from open file descriptors
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        with open(str(in_path), "r") as my_open_file:
            w_list = WordList(my_open_file)
            result = tuple(w_list)
        assert ("foo", "bar", "-dash-at-start", "baz") == result

    def test_detect_unsigned_wordlists(self, tmpdir):
        # we can detect unsigned wordlist files.
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("foo\n")
        w_list = WordList(str(in_file))
        assert w_list.signed is False

    def test_detect_signed_wordlists(self):
        # we can detect signed wordlist files.
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        w_list = WordList(in_path)
        assert w_list.signed is True

    def test_wordlists_are_generators(self, tmpdir):
        # WordList instances act like generators.
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("foo\nbar\n")
        w_list = WordList(str(in_file))
        assert list(w_list) == ["foo", "bar"]

    def test_wordlist_from_signed_file(self):
        # we can get an iterator from signed wordlist.
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        w_list = WordList(in_path)
        assert list(w_list) == ["foo", "bar", "-dash-at-start", "baz"]

    def test_wordlist_en_8k(self):
        # we can get a list of words out of the reinhold english 8k wordlist.
        en_src = os.path.join(WORDLISTS_DIR, 'wordlist_en.txt')
        w_list = WordList(en_src)
        long_list = list(w_list)
        assert long_list[0] == "a"
        assert long_list[-1] == "@"
        assert len(long_list) == 8192

    def test_wordlist_en_securedrop(self):
        # we can get a list of words out of securedrop english 8k wordlist.
        en_src = os.path.join(WORDLISTS_DIR, 'wordlist_en_securedrop.asc')
        w_list = WordList(en_src)
        long_list = list(w_list)
        assert long_list[0] == "0"
        assert long_list[-1] == "zurich"
        assert len(long_list) == 8192

    def test_wordlist_en(self):
        # we can get a list of words out of the original diceware wordlist.
        en_src = os.path.join(WORDLISTS_DIR, 'wordlist_en_orig.asc')
        w_list = list(WordList(en_src))
        assert w_list[0] == "a"
        assert w_list[-1] == "@"
        assert len(w_list) == 7776

    def test_wordlist_en_eff(self):
        # we can get a list of words out of the EFF-maintained wordlist.
        en_src = os.path.join(WORDLISTS_DIR, 'wordlist_en_eff.txt')
        w_list = list(WordList(en_src))
        assert w_list[0] == "abacus"
        assert w_list[-1] == "zoom"
        assert len(w_list) == 7776

    def test_get_wordlist_simple(self, tmpdir):
        # simple wordlists can be created
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("a\nb\n")
        result = list(WordList(str(in_file)))
        assert ['a', 'b'] == result

    def test_get_wordlist_ignore_empty_lines(self, tmpdir):
        # we ignore empty lines in wordlists
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("\n\na\n\n")
        result = list(WordList(str(in_file)))
        assert ['a'] == result

    def test_get_signed_wordlist_handles_clearsigned_files(self):
        # we can process cryptogrphically signed files
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        with open(in_path, 'r') as fd:
            result = list(WordList(fd))
        assert ["foo", "bar", "-dash-at-start", "baz"] == result

    def test_get_signed_wordlist_handles_en_orig(self):
        # we can process the original diceware list from diceware.com
        wlist_path = os.path.join(WORDLISTS_DIR, 'wordlist_en_orig.asc')
        w_list = WordList(wlist_path)
        result = list(w_list)
        assert len(result) == 7776
        assert "a" == result[0]
        assert "@" == result[-1]

    def test_get_signed_wordlist_ignore_empty_lines(self):
        # we ignore empty lines in wordlists
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        w_list = WordList(in_path)
        result = list(w_list)
        assert '' not in result

    def test_can_get_wordlist_multiple_times(self, tmpdir):
        # we can get a wordlist several times
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("\n\na\n\n")
        w_list = WordList(str(in_file))
        list1 = list(w_list)
        list2 = list(w_list)
        assert list1 == list2

    def test_can_get_wordlist_multiple_times_from_fd(self, tmpdir):
        # we can get a wordlist several times also if it is a fd.
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("foo\nbar\n")
        with open(str(in_file), "r") as fd:
            w_list = WordList(fd)
            list1 = list(w_list)
            list2 = list(w_list)
        assert list1 == list2

    def test_is_signed_detects_signed_files(self):
        # we recognize signed wordlists
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        with open(in_path, "r") as fd:
            w_list = WordList(fd)
            w_list.fd = fd
            result = w_list.is_signed()
        assert result is True

    def test_is_signed_detects_unsigned_files(self, tmpdir):
        # we can tell if a wordlist is not signed
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("a\nb\n")
        with open(in_file.strpath, 'r') as fd:
            w_list = WordList(fd)
            w_list.fd = fd
            result = w_list.is_signed()
        assert result is False

    def test_refine_entry_strips(self, wordlist):
        # we strip() entries
        assert wordlist.refine_entry("foo") == "foo"
        assert wordlist.refine_entry(" foo \n") == "foo"
        assert wordlist.refine_entry(" foo bar \n") == "foo bar"

    def test_refine_entry_handles_numbered(self, wordlist):
        # we transform numbered lines
        assert wordlist.refine_entry("11111\tfoo") == "foo"

    def test_refine_entry_handles_dash_quotes_when_signed(
            self, wordlist):
        # we handle dash-escaped lines correctly when in signed mode
        assert wordlist.refine_entry("- foo") == "- foo"
        wordlist.signed = True
        assert wordlist.refine_entry("- foo") == "foo"

    def test_refine_entry_strips_also_dash_quoted(self, wordlist):
        # also dash-escaped lines in signed wordlistgs are stripped.
        wordlist.signed = True
        assert wordlist.refine_entry("- \tfoo\n") == "foo"

    def test_refine_entry_strips_also_numbered(self, wordlist):
        # also numbered entries are stripped
        assert wordlist.refine_entry("11111 \t foo\n") == "foo"

    def test_refine_entry_can_handle_all_at_once(self, wordlist):
        # we can do all the things above at once and in right order.
        wordlist.signed = True
        assert wordlist.refine_entry("- 11111 foo  \n") == "foo"
