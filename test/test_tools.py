import unittest

from mcomix import tools


class TestAlphanumericSort(unittest.TestCase):
    def test_numbers_are_ordered_naturally(self) -> None:
        lst = ['10.jpg', '2.jpg']
        tools.alphanumeric_sort(lst)
        self.assertListEqual(lst, ['2.jpg', '10.jpg'])

    def test_sort_with_mixed_number_and_string_files(self) -> None:
        lst = ['text_2.jpg', '2_text.jpg']
        tools.alphanumeric_sort(lst)
        self.assertListEqual(lst, ['2_text.jpg', 'text_2.jpg'])

    def test_sort_creates_strict_order(self) -> None:
        lst = ['Comic 001-01.jpg', 'Comic 001-00.jpg', 'zCover.jpg', 'Comic 001-03.jpg']
        tools.alphanumeric_sort(lst)
        self.assertListEqual(lst, ['Comic 001-00.jpg', 'Comic 001-01.jpg', 'Comic 001-03.jpg', 'zCover.jpg'])
