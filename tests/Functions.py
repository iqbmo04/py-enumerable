__author__ = 'Viralogic Software'

from unittest import TestCase
from py_linq import Enumerable
from tests import _empty, _simple, _complex, _locations
from py_linq.exceptions import *


class TestFunctions(TestCase):
    def setUp(self):
        self.empty = Enumerable(_empty)
        self.simple = Enumerable(_simple)
        self.complex = Enumerable(_complex)

    def test_to_list(self):
        empty_list = self.empty.to_list()
        simple_list = self.simple.to_list()
        complex_list = self.complex.to_list()

        self.assertIsInstance(empty_list, list, "Empty enumerable not converted to list")
        self.assertIsInstance(simple_list, list, "Simple enumerable not converted to list")
        self.assertIsInstance(complex_list, list, "Complex enumerable not converted to list")

        self.assertEqual(len(empty_list), 0, "Empty enumerable has 0 elements")
        self.assertEqual(len(simple_list), 3, "Simple enumerable has 3 elements")
        self.assertEqual(len(complex_list), 3, "Complex enumerable has 3 elements")

    def test_sum(self):
        self.assertEqual(self.empty.sum(), 0, "Sum of empty enumerable should be 0")
        self.assertEqual(self.simple.sum(), 6, "Sum of simple enumerable should be 6")
        self.assertEqual(self.complex.sum(lambda x: x['value']), 6, "Sum of complex enumerable should be 6")

    def test_count(self):
        self.assertEqual(self.empty.count(), 0, "Empty enumerable has 0 elements")
        self.assertEqual(self.simple.count(), 3, "Simple enumerable has 3 elements")
        self.assertEqual(self.complex.count(), 3, "Complex enumerable has 3 elements")

    def test_select(self):
        self.assertEqual(self.empty.select(lambda x: x['value']).count(), 0, "Empty enumerable should still have 0 elements")

        self.assertRaises(NullArgumentError, self.simple.select, None)
        simple_select = self.simple.select(lambda x: { 'value' : x }).to_list()
        first_simple = simple_select[0]
        simple_count = len(simple_select)
        self.assertIsInstance(first_simple, dict, "Transformed simple enumerable element is dictionary")
        self.assertEqual(simple_count, 3, "Transformed simple enumerable has 3 elements")


        complex_select = self.complex.select(lambda x: x['value']).to_list()
        first_complex = complex_select[0]
        complex_count = len(complex_select)
        self.assertEqual(complex_count, 3, "Transformed complex enumerable has 3 elements")
        self.assertIsInstance(first_complex, int, "Transformed complex enumerable element is integer")

    def test_max_min(self):
        self.assertRaises(NoElementsError, self.empty.min)
        self.assertEqual(self.simple.min(), 1, "Minimum value of simple enumerable is 1")
        self.assertEqual(self.complex.min(lambda x: x['value']), 1, "Min value of complex enumerable is 1")

        self.assertRaises(NoElementsError, self.empty.max)
        self.assertEqual(self.simple.max(), 3, "Max value of simple enumerable is 3")
        self.assertEqual(self.complex.max(lambda x: x['value']), 3, "Max value of complex enumerable is 3")

    def test_avg(self):
        avg = float(2)
        self.assertRaises(NoElementsError, self.empty.avg)
        self.assertEqual(self.simple.avg(), avg, "Avg value of simple enumerable is {0:.5f}".format(avg))
        self.assertEqual(self.complex.avg(lambda x: x['value']), avg, "Avg value of complex enumerable is {0:.5f}".format(avg))

    def test_first_last(self):
        self.assertRaises(NoElementsError, self.empty.first)
        self.assertEqual(self.empty.first_or_default(), None, "First or default should be None")
        self.assertIsInstance(self.simple.first(), int, "First element in simple enumerable is int")
        self.assertEqual(self.simple.first(), 1, "First element in simple enumerable is 1")
        self.assertEqual(self.simple.first(), self.simple.first_or_default(), "First and first or default should equal")
        self.assertIsInstance(self.complex.first(), dict, "First element in complex enumerable is dict")
        self.assertDictEqual(self.complex.first(), {'value': 1}, "First element in complex enumerable is not correct dict")
        self.assertDictEqual(self.complex.first(), self.complex.first_or_default(), "First and first or default should equal")
        self.assertEqual(self.simple.first(), self.complex.select(lambda x: x['value']).first(), "First values in simple and complex should equal")


        self.assertRaises(NoElementsError, self.empty.last)
        self.assertEqual(self.empty.last_or_default(), None, "Last or default should be None")
        self.assertIsInstance(self.simple.last(), int, "Last element in simple enumerable is int")
        self.assertEqual(self.simple.last(), 3, "Last element in simple enumerable is 3")
        self.assertEqual(self.simple.last(), self.simple.last_or_default(), "Last and last or default should equal")
        self.assertIsInstance(self.complex.last(), dict, "Last element in complex enumerable is dict")
        self.assertDictEqual(self.complex.last(), {'value': 3}, "Last element in complex enumerable is not correct dict")
        self.assertDictEqual(self.complex.last(), self.complex.last_or_default(), "Last and last or default should equal")
        self.assertEqual(self.simple.last(), self.complex.select(lambda x: x['value']).last(), "Last values in simple and complex should equal")

    def test_sort(self):
        self.assertRaises(NullArgumentError, self.simple.order_by, None)
        self.assertRaises(NullArgumentError, self.simple.order_by_descending, None)

        self.assertListEqual(self.simple.order_by(lambda x: x).to_list(), self.simple.to_list(), "Simple enumerable sort ascending should yield same list")
        self.assertListEqual(self.simple.order_by_descending(lambda x: x).to_list(), sorted(self.simple, key=lambda x: x, reverse=True), "Simple enumerable sort descending should yield reverse list")

        self.assertListEqual(self.complex.order_by(lambda x: x['value']).to_list(), self.complex.to_list(), "Complex enumerable sort ascending should yield same list")
        self.assertListEqual(self.complex.order_by_descending(lambda x: x['value']).to_list(), sorted(self.complex, key=lambda x: x['value'], reverse=True), "Complex enumerable sort descending should yield reverse list")

        self.assertListEqual(self.simple.order_by(lambda x: x).to_list(), self.complex.select(lambda x: x['value']).order_by(lambda x: x).to_list(), "Projection and sort ascending of complex should yield simple")

    def test_median(self):
        self.assertRaises(NoElementsError, self.empty.median)

        median = float(2)
        self.assertEqual(self.simple.median(), median, "Median of simple enumerable should be {0:.5f}".format(median))
        self.assertEqual(self.complex.median(lambda x: x['value']), median, "Median of complex enumerable should be {0:.5f}".format(median))

    def test_skip_take(self):
        self.assertListEqual(self.empty.skip(2).to_list(), [], "Skip 2 of empty list should yield empty list")
        self.assertListEqual(self.empty.take(2).to_list(), [], "Take 2 of empty list should yield empty list")

        self.assertEqual(self.simple.skip(1).take(1).first(), 2, "Skip 1 and take 1 of simple should yield 2")
        self.assertEqual(self.complex.select(lambda x: x['value']).skip(1).take(1).first(), 2, "Skip 1 and take 1 of complex with projection should yield 2")

    def test_filter(self):
        self.assertListEqual(self.empty.where(lambda x: x == 0).to_list(), [], "Filter on empty list should yield empty list")
        self.assertListEqual(self.simple.where(lambda x: x==2).to_list(), [2], "Filter where element equals 2 should yield list with one element")
        self.assertListEqual(self.complex.where(lambda x: x['value'] == 2).to_list(), [{'value':2}], "Filter where element value is 2 should yield list with one element")
        self.assertListEqual(self.complex.where(lambda x: x['value'] == 2).select(lambda x: x['value']).to_list(), self.simple.where(lambda x: x == 2).to_list(), "Filter and projection of complex enumerable should equal filter of simple enumerable")
        self.assertListEqual(self.simple.where(lambda x: x== 0).to_list(), self.empty.to_list(), "Filter simple enumerable with no matching elements yields empty list")

    def test_single_single_or_default(self):
        self.assertRaises(NullArgumentError, self.empty.single, None)

        self.assertRaises(NoMatchingElement, self.empty.single, lambda x: x == 0)
        self.assertRaises(NoMatchingElement, self.simple.single, lambda x: x == 0)
        self.assertRaises(NoMatchingElement, self.complex.single, lambda x: x['value'] == 0)

        self.assertRaises(MoreThanOneMatchingElement, self.simple.single, lambda x: x > 0)
        self.assertRaises(MoreThanOneMatchingElement, self.complex.single, lambda x: x['value'] > 0)

        self.assertRaises(MoreThanOneMatchingElement, self.simple.single_or_default, lambda x: x > 0)
        self.assertRaises(MoreThanOneMatchingElement, self.complex.single_or_default, lambda x: x['value'] > 0)

        simple_single = self.simple.single(lambda x: x == 2)
        self.assertIsInstance(simple_single, int, "Single on simple enumerable where element value equals 2 should yield int")
        self.assertEqual(simple_single, 2, "Single on simple enumerable where element value equals 2 should yield 2")

        complex_single = self.complex.single(lambda x: x['value'] == 2)
        self.assertIsInstance(complex_single, dict, "Single on complex enumerable where element value equals 2 should yield dict")
        self.assertDictEqual(complex_single, {'value': 2}, "Single on complex enumerable where element value equals 2 should yield '{'value':2}'")
        self.assertEqual(simple_single, self.complex.select(lambda x: x['value']).single(lambda x: x == 2), "Projection and single on complex should yield single on simple")

        self.assertEqual(self.empty.single_or_default(lambda x: x == 0), None, "Single or default on empty list should yield None")
        self.assertEqual(self.simple.single_or_default(lambda x: x == 0), None, "Single or default filtering on simple enumerable with element value equals 0 should yield None")
        self.assertEqual(self.complex.single_or_default(lambda x: x['value'] == 0), None, "Single or default filtering on complex enumerable with element value equals 0 should yield None")

    def test_select_many(self):
        _empty = Enumerable([[], [], []])
        _simple = Enumerable([[1,2,3], [4,5,6], [7,8,9]])
        _complex = Enumerable([{'key': 1, 'values': [1,2,3]}, {'key': 2, 'values': [4,5,6]}, {'key': 3, 'values': [7,8,9]}])

        self.assertListEqual(_empty.select_many().to_list(), [], "Select many of enumerable of empty lists should yield empty list")
        self.assertListEqual(_simple.select_many().to_list(), [1,2,3,4,5,6,7,8,9], "Select many of enumerable of simple lists should yield simple enumerable with single list")
        self.assertListEqual(_complex.select_many(lambda x: x['values']).to_list(), _simple.select_many().to_list(), "Select many of enumerable of complex list should yield simple enumerable with single list")

    def test_concat(self):
        self.assertListEqual(self.empty.concat(self.empty).to_list(), [], "Concatenation of 2 empty lists gives empty list")
        self.assertListEqual(self.empty.concat(self.simple).to_list(), _simple, "Concatenation of empty to simple yields simple")
        self.assertListEqual(self.simple.concat(self.empty).to_list(), _simple, "Concatenation of simple to empty yields simple")
        self.assertListEqual(self.simple.concat(self.complex).to_list(), _simple + _complex, "Concatentation of simple to complex yields simple + complex")

    def test_group_by(self):
        self.assertRaises(Exception, self.empty.group_by, lambda x: x)

        simple_grouped = self.simple.group_by().to_list()
        self.assertEqual(simple_grouped.count(), 3, "Three grouped elements in simple grouped")
        for g in simple_grouped:
            self.assertEqual(g.key.id, g.first(), "Each id in simple grouped should match first value")








