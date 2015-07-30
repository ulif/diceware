import os
import pytest
from diceware.wordlist import (
    WORDLISTS_DIR, RE_WORDLIST_NAME, RE_NUMBERED_WORDLIST_ENTRY, get_wordlist,
    get_signed_wordlist, get_wordlist_path, get_wordlist_names,
    is_signed_wordlist, refine_wordlist_entry, WordList,
)


@pytest.fixture(scope="function")
def wordlists_dir(request, monkeypatch, tmpdir):
    """This fixture provides a temporary wordlist dir.
    """
    monkeypatch.setattr("diceware.wordlist.WORDLISTS_DIR", str(tmpdir))
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


class Test_GetSignedWordList(object):

    def test_get_signed_wordlist_handles_clearsigned_files(self, tmpdir):
        # we can process cryptogrphically signed files
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        with open(in_path, 'r') as fd:
            result = get_signed_wordlist(fd)
        assert ["foo", "bar", "-dash-at-start", "baz"] == result

    def test_get_signed_wordlist_handles_en_orig(self, tmpdir):
        # we can process the original diceware list from diceware.com
        wlist_path = os.path.join(WORDLISTS_DIR, 'wordlist_en_orig.asc')
        with open(wlist_path, 'r') as fd:
            result = get_signed_wordlist(fd)
        assert len(result) == 7776
        assert "a" == result[0]
        assert "@" == result[-1]

    def test_get_signed_wordlist_ignore_empty_lines(self, tmpdir):
        # we ignore empty lines in wordlists
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        with open(in_path, 'r') as fd:
            result = get_signed_wordlist(fd)
        assert '' not in result

    def test_get_signed_wordlist_closes_fd(self, tmpdir):
        # we close passed-in file descriptors
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        with open(in_path, 'r') as fd:
            get_signed_wordlist(fd)
            assert fd.closed is True


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
        assert RE_NUMBERED_WORDLIST_ENTRY.match('11111   a') is not None
        assert RE_NUMBERED_WORDLIST_ENTRY.match(
            '11111   a').groups() == ('a', )
        assert RE_NUMBERED_WORDLIST_ENTRY.match('12211\t 1') is not None
        assert RE_NUMBERED_WORDLIST_ENTRY.match(
            '12211\t 1').groups() == ('1', )
        assert RE_NUMBERED_WORDLIST_ENTRY.match('12a11 foo') is None
        assert RE_NUMBERED_WORDLIST_ENTRY.match('foo bar') is None

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

    def test_is_signed_wordlist(self):
        # we recognize signed wordlists
        in_path = os.path.join(
            os.path.dirname(__file__), "sample_signed_wordlist.asc")
        with open(in_path, "r") as fd:
            result = is_signed_wordlist(fd)
        assert result is True

    def test_is_signed_wordlist_plain(self, tmpdir):
        # we can tell if a wordlist is not signed
        in_file = tmpdir.mkdir("work").join("mywordlist")
        in_file.write("a\nb\n")
        with open(in_file.strpath, 'r') as fd:
            result = is_signed_wordlist(fd)
        assert result is False

    def test_refine_wordlist_entry_strips(self):
        # we strip() entries
        assert refine_wordlist_entry("foo") == "foo"
        assert refine_wordlist_entry(" foo \n") == "foo"
        assert refine_wordlist_entry(" foo bar \n") == "foo bar"

    def test_refine_wordlist_entry_handles_numbered(self):
        # we transform numbered lines
        assert refine_wordlist_entry("11111\tfoo") == "foo"

    def test_refine_wordlist_entry_handles_dash_quotes_when_signed(self):
        # we handle dash-escaped lines correctly when in signed mode
        assert refine_wordlist_entry("- foo") == "- foo"
        assert refine_wordlist_entry("- foo", signed=True) == "foo"

    def test_refine_wordlist_strips_also_dash_quoted(self):
        # also dash-escaped lines in signed wordlistgs are stripped.
        assert refine_wordlist_entry("- \tfoo\n", signed=True) == "foo"

    def test_refine_wordlist_strips_also_numbered(self):
        # also numbered entries are stripped
        assert refine_wordlist_entry("11111 \t foo\n") == "foo"


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
        # we can get a list of words out of english 8k wordlist.
        en_src = os.path.join(WORDLISTS_DIR, 'wordlist_en_8k.txt')
        w_list = WordList(en_src)
        long_list = list(w_list)
        assert long_list[0] == "a"
        assert long_list[-1] == "@"
        assert len(long_list) == 8192

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
            result = get_signed_wordlist(fd)
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
