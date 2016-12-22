from __future__ import unicode_literals
import pkg_resources
import pytest
import sys
import argparse
from conftest import InputMock
from io import StringIO
from diceware import main
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
        # late import, because we need the patched version
        from diceware.random_sources import input_func
        result1 = input_func("Enter some values: ")
        assert result1 == "foo"
        result2 = input_func("Enter more values: ")
        assert result2 == "bar"
        out, err = capsys.readouterr()             # captured stdout/stderr
        assert out == "Enter some values: foo\nEnter more values: bar\n"

    def test_options_are_stored(self):
        # options passed-in are stored with RealDiceRandomSource instances
        options = "fake_check"
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
        expected_index = 6 * (1 - 1) + (2 - 1)     # = 6 x roll_1 + roll_2 - 1
        assert src.choice(sequence) == sequence[expected_index]

    def test_choice_num_of_dice_for_seq_len216(self, monkeypatch):
        # choice() requires three dice for a sequence len of 6**3
        self.fake_input_values(["1", "2", "3"], monkeypatch)
        src = RealDiceRandomSource(None)
        sequence = list(range(6 ** 3))        # 216
        # = 6^2 * (roll_1 - 1) + 6^1 * (roll_2 - 1) + (roll_3 - 1)
        expected_index = 0 + 6 + 3 - 1
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
        assert "Using only first 6 of 7 words" in out
        assert err == ""

    def test_no_hint_if_entropy_is_not_decreased(self, monkeypatch, capsys):
        # we do not issue the entropy warning if not neccessary
        self.fake_input_values(["1"] * 6, monkeypatch)
        src = RealDiceRandomSource(None)
        picked1 = src.choice([1, 2, 3, 4, 5, 6])
        picked2 = src.choice(range(1, 6 ** 2 + 1))
        picked3 = src.choice(range(1, 6 ** 3 + 1))
        assert picked1 == 1
        assert picked2 == 1
        assert picked3 == 1
        out, err = capsys.readouterr()
        assert "entropy is reduced" not in out
        assert err == ""

    def test_non_numbers_as_input_are_rejected(self, monkeypatch):
        # Users might input non-numbers. We ask again then.
        self.fake_input_values(["no-number", "", "1"], monkeypatch)
        src = RealDiceRandomSource(None)
        assert src.choice([1, 2, 3, 4, 5, 6]) == 1

    def test_choice_input_lower_value_borders(self, monkeypatch):
        # choice() does not accept "0" but it accepts "1"
        self.fake_input_values(["0", "1"], monkeypatch)
        src = RealDiceRandomSource(None)
        sequence = (1, 2, 3, 4, 5, 6)
        assert src.choice(sequence) == 1

    def test_choice_input_upper_value_borders(self, monkeypatch):
        # choice() does not accept "7" but it accepts "6"
        self.fake_input_values(["7", "6"], monkeypatch)
        src = RealDiceRandomSource(None)
        sequence = (1, 2, 3, 4, 5, 6)
        assert src.choice(sequence) == 6

    def test_pre_check_no_rolls_cause_exception(self):
        # we cannot pick zero items of a sequence
        src = RealDiceRandomSource(None)
        with pytest.raises(ValueError):
            src.pre_check(0, list(range(6)))

    def test_pre_check_warn_if_not_all_seq_items_used(self, capsys):
        # we issue a warning if not all sequence items will be used
        src = RealDiceRandomSource(None)
        src.dice_sides = 10
        src.pre_check(1, list(range(10)))
        out, err = capsys.readouterr()
        assert "entropy is reduced" not in out
        src.pre_check(1, list(range(11)))
        out, err = capsys.readouterr()
        assert "entropy is reduced" in out

    def test_pre_check_requests_rolling_dice(self, capsys):
        # we request the user to roll dice
        src = RealDiceRandomSource(None)
        src.pre_check(5, ['doesntmatter'])
        out, err = capsys.readouterr()
        assert "Please roll 5 dice (or a single dice 5 times)." in out

    def test_sequence_less_than_dice_sides(self, capsys, monkeypatch):
        # Test to see whether we can use a n-sided die to choose from
        # a sequence with less than n items
        src = RealDiceRandomSource(None)
        src.dice_sides = 6
        # A length of 1 requires no rolls
        self.fake_input_values(["1"], monkeypatch)
        picked = src.choice([1])
        out, err = capsys.readouterr()
        assert "roll" not in out
        assert picked == 1
        # A length of 2,3 only requires 1 roll
        for choice_length in (2, 3):
            self.fake_input_values(["1"], monkeypatch)
            picked = src.choice(range(1, choice_length + 1))
            out, err = capsys.readouterr()
            assert "roll 1 dice" in out
            assert picked == 1
        # A length of 4,5 requires 2 rolls
        for choice_length in (4, 5):
            self.fake_input_values(["1", "1"], monkeypatch)
            picked = src.choice(range(1, choice_length + 1))
            out, err = capsys.readouterr()
            assert "roll 2 dice" in out
            assert picked == 1

    def test_dice_sides_respected(self, capsys, monkeypatch):
        # we use the number of dice sides given by options dict.
        self.fake_input_values(["1", "2"], monkeypatch)
        # A Namespace, not a dict, is passed to the constructor.
        options = argparse.Namespace(dice_sides=2)  # a coin
        src = RealDiceRandomSource(options)
        picked = src.choice(['a', 'b', 'c', 'd'])
        out, err = capsys.readouterr()
        # must throw a coin 2 times to pick one out of 4 items
        assert "Please roll 2 dice" in out
        assert picked == 'b'

    def test_main_with_realdice_source(
            self, argv_handler, capsys, monkeypatch):
        # we can run main with `realdice` source of randomness
        self.fake_input_values(
            ["1", "3"], monkeypatch)
        sys.stdin = StringIO("w1\nw2\nw3\nw4\nw5\nw6\n")
        sys.argv = ['diceware', '-r', 'realdice', '-n', '2', '-d', '#', '-']
        main()
        out, err = capsys.readouterr()
        assert out.endswith('W1#W3\n')
