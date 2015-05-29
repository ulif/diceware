import pkg_resources
from diceware.random_sources import SystemRandomSource


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
