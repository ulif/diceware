import pkg_resources
import pytest

from diceware.random_sources import (
    SystemRandomSource, RealDiceRandomSource,
    )


class TestSystemRandomSource(object):

    def test_options_are_stored(self):
        # options passed-in are stored with SystemRandomStource instances
        options = "fake_options"
        src = SystemRandomSource(options)
        assert src.options is options

    def test_has_choice_method(self):
        # SystemRandomInstances provide a choice method
        src = SystemRandomSource(None)
        assert hasattr(src, 'choice')

    def test_registered_as_system(self):
        # The SystemRandomInstance is registered as entry point with
        # name 'system' in group 'diceware_random_sources'
        sources_dict = dict()
        for entry_point in pkg_resources.iter_entry_points(
                group="diceware_random_sources"):
            sources_dict.update({entry_point.name: entry_point.load()})
        assert 'system' in sources_dict
        assert sources_dict['system'] == SystemRandomSource

    def test_choice_accepts_lists_of_numbers(self):
        # the choice() method accepts lists of numbers
        src = SystemRandomSource(None)
        assert src.choice([1, 2, 3]) in [1, 2, 3]

    def test_choice_accepts_tuples_of_numbers(self):
        # the choce() method accepts tuples of numbers
        src = SystemRandomSource(None)
        assert src.choice((1, 2, 3), ) in [1, 2, 3]

    def test_choice_accepts_list_of_chars(self):
        # the choice() method accepts lists of chars
        src = SystemRandomSource(None)
        assert src.choice(['a', 'b', 'c']) in ['a', 'b', 'c']

    def test_choice_accepts_list_of_strings(self):
        # the choice() method accepts lists of strings
        src = SystemRandomSource(None)
        assert src.choice(['foo', 'bar', 'baz']) in ['foo', 'bar', 'baz']

    def test_choice_picks_all_items(self):
        # make sure all items of a sequence are picked (in the long run)
        sequence = [1, 2, 3, 4]
        picked = set()
        num = 10 ** 3
        src = SystemRandomSource(None)
        while num:
            picked.add(src.choice(sequence))
            if len(picked) == len(sequence):
                break
            num -= 1
        assert num > 0


class InputMock(object):
    """A replacement for input() or raw_input() respectively.

    This mock, when called, mimics input() behaviour, outputs a prompt,
    etc., but does not wait for real key strokes. Instead it returns the
    next value from `fake_input_values` given on initialization:

       >>> faked_input = InputMock(["val1", "val2", "1"])
       >>> faked_input("Give a value: ")
       Give a value: val1
       'val1'

       >>> faked_input("And another value: ")
       And another value: val2
       'val2'

       >>> faked_input()
       1
       '1'

    To be used with the `monkeypatch` pytest fixture, to replace
    `diceware.random_sources.input_func`.
    """
    fake_input_values = []

    def __init__(self, fake_input_values=[]):
        self.fake_input_values = fake_input_values
        self.fake_input_values.reverse()

    def __call__(self, prompt=''):
        curr_value = self.fake_input_values.pop()
        print("%s%s" % (prompt, curr_value))
        return curr_value


class TestRealDiceRandomSource(object):

    @classmethod
    def fake_input_values(cls, values, patch):
        input_mock = InputMock(values)
        patch.setattr(
            # function to replace, replacement
            "diceware.random_sources.input_func", input_mock)
        return input_mock

    def test_raw_input_patch_works(self, monkeypatch, capsys):
        # make sure our fake input works. We try to fake input ('foo',
        # 'bar') and make sure that output is captured.
        # This test is just a hint, how input could be faked in real tests.
        # It can (and should) be removed if not needed any more.
        self.fake_input_values(["foo", "bar"], monkeypatch)
        dice_src = RealDiceRandomSource(None)
        result1 = dice_src.get_input()
        assert result1 == "foo"
        result2 = dice_src.get_input()
        assert result2 == "bar"
        out, err = capsys.readouterr()             # captured stdout/stderr
        assert out == "Enter some values: foo\nEnter some values: bar\n"

    def test_options_are_stored(self):
        # options passed-in are stored with RealDiceRandomSource instances
        options = "fake_options"
        src = RealDiceRandomSource(options)
        assert src.options is options

    def test_has_choice_method(self):
        # RealDiceRandomSource instances provide a choice method
        src = RealDiceRandomSource(None)
        assert hasattr(src, 'choice')

    def test_registered_as_realdice(self):
        # The RealDiceRandomSource is registered as entry point with
        # name 'realdice' in group 'diceware_random_sources'
        sources_dict = dict()
        for entry_point in pkg_resources.iter_entry_points(
                group="diceware_random_sources"):
            sources_dict.update({entry_point.name: entry_point.load()})
        assert 'realdice' in sources_dict
        assert sources_dict['realdice'] == RealDiceRandomSource

    def test_choice_accepts_lists_of_numbers(self, monkeypatch):
        # the choice() method accepts lists of numbers
        self.fake_input_values(["1"], monkeypatch)
        src = RealDiceRandomSource(None)
        assert src.choice([11, 12, 13, 14, 15, 16]) == 11

    def test_choice_accepts_tuples_of_numbers(self, monkeypatch):
        # the choice() method accepts tuples of numbers
        self.fake_input_values(["1"], monkeypatch)
        src = RealDiceRandomSource(None)
        assert src.choice((11, 12, 13, 14, 15, 16), ) == 11

    def test_choice_accepts_list_of_chars(self, monkeypatch):
        # the choice() method accepts lists of chars
        self.fake_input_values(["1"], monkeypatch)
        src = RealDiceRandomSource(None)
        assert src.choice(['a', 'b', 'c', 'd', 'e', 'f']) == 'a'

    def test_choice_accepts_list_of_strings(self, monkeypatch):
        # the choice() method accepts lists of strings
        self.fake_input_values(["1"], monkeypatch)
        src = RealDiceRandomSource(None)
        assert src.choice(
            ['val1', 'val2', 'val3', 'val4', 'val5', 'val6']) == "val1"

    def test_choice_num_of_dice_for_seq_len36(self, monkeypatch):
        # choice() requires two dice for a sequence len of 6**2
        self.fake_input_values(["1", "2"], monkeypatch)
        src = RealDiceRandomSource(None)
        sequence = list(range(6 ** 2))
        expected_index = 1 * 2 - 1          # = roll_1 x roll_2 - 1
        assert src.choice(sequence) == sequence[expected_index]

    def test_choice_num_of_dice_for_seq_len216(self, monkeypatch):
        # choice() requires three dice for a sequence len of 6**3
        self.fake_input_values(["1", "2", "3"], monkeypatch)
        src = RealDiceRandomSource(None)
        sequence = list(range(6 ** 3))        # 216
        expected_index = 1 * 2 * 3 - 1        # = roll_1 x roll_2 x roll_3 - 1
        assert src.choice(sequence) == sequence[expected_index]

    def test_hint_if_entropy_is_decreased(self, monkeypatch, capsys):
        # if len of choice is not a multiple of 6, entropy is decreased
        # (not the whole sequence is taken into consideration). We get
        # a warning in that case.
        self.fake_input_values(["1"], monkeypatch)
        src = RealDiceRandomSource(None)
        picked = src.choice([1, 2, 3, 4, 5, 6, 7])
        assert picked == 1
        out, err = capsys.readouterr()
        assert "entropy is reduced" in out
        assert err == ""

    def test_non_numbers_as_input_are_rejected(self, monkeypatch):
        # Users might input non-numbers. We ask again then.
        self.fake_input_values(["no-number", "", "1"], monkeypatch)
        src = RealDiceRandomSource(None)
        assert src.choice([1, 2, 3, 4, 5, 6]) == 1

    def test_choice_len_too_short(self, monkeypatch):
        # We raise an exception if choice gets less than 6 elements.
        self.fake_input_values(["1"], monkeypatch)
        src = RealDiceRandomSource(None)
        with pytest.raises(ValueError):
            assert src.choice([1, 2, 3, 4, 5])  # list len < 6
