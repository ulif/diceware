import pkg_resources

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


class TestRealDiceSource(object):

    def test_raw_input_patch_works(self, monkeypatch, capsys):
        # make sure our fake input works. We try to fake input ('foo',
        # 'bar') and make sure that output is captured.
        # This test is just a hint, how input could be faked in real tests.
        # It can (and should) be removed if not needed any more.
        monkeypatch.setattr(
            "diceware.random_sources.input_func",  # function to replace
            InputMock(["foo", "bar"]))             # faked input values
        dice_src = RealDiceRandomSource()
        result1 = dice_src.get_input()
        assert result1 == "foo"
        result2 = dice_src.get_input()
        assert result2 == "bar"
        out, err = capsys.readouterr()             # captured stdout/stderr
        assert out == "Enter some values: foo\nEnter some values: bar\n"
