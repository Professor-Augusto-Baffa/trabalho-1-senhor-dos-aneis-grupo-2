import typing
from src.utils import *

import unittest

class MinHeapTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MinHeapTestCase, self).__init__(*args, **kwargs)
        self.min_heap: typing.Optional[MinHeap[int]]

    def setUp(self) -> None:
        self.min_heap = MinHeap()
        self.min_heap.push(3, 3)
        self.min_heap.push(1, 1)
        self.min_heap.push(2, 2)
    
    def test_add_and_remove_one(self) -> None:
        new_heap: MinHeap[int] = MinHeap()
        self.assertTrue(new_heap.is_empty())
        new_heap.push(5, 5)
        self.assertFalse(new_heap.is_empty())
        self.assertEqual(new_heap.peek(), 5)
        self.assertFalse(new_heap.is_empty())
        self.assertEqual(new_heap.pop(), 5)
        self.assertTrue(new_heap.is_empty())
        with self.assertRaises(IndexError):
            new_heap.pop()
        with self.assertRaises(IndexError):
            new_heap.peek()

    def test_removals_happen_in_order(self) -> None:
        self.assertEqual(self.min_heap.peek(), 1)
        self.assertEqual(self.min_heap.pop(), 1)
        self.assertEqual(self.min_heap.peek(), 2)
        self.assertEqual(self.min_heap.pop(), 2)
        self.assertEqual(self.min_heap.peek(), 3)
        self.assertEqual(self.min_heap.pop(), 3)
    
    def test_add_and_remove_many(self) -> None:
        self.assertEqual(self.min_heap.peek(), 1)
        self.min_heap.push(0, 0)
        self.assertEqual(self.min_heap.peek(), 0)
        self.assertEqual(self.min_heap.pop(), 0)
        self.assertEqual(self.min_heap.pop(), 1)
        self.assertEqual(self.min_heap.peek(), 2)
        self.min_heap.push(4, 4)
        self.min_heap.push(6, 6)
        self.min_heap.push(5, 5)
        self.assertEqual(self.min_heap.peek(), 2)
        self.assertEqual(self.min_heap.pop(), 2)
        self.assertEqual(self.min_heap.pop(), 3)
        self.assertEqual(self.min_heap.pop(), 4)
        self.assertEqual(self.min_heap.pop(), 5)
        self.assertEqual(self.min_heap.pop(), 6)
        with self.assertRaises(IndexError):
            self.min_heap.pop()
        
    def test_in_operator(self):
        self.assertIn(1, self.min_heap)
        self.assertIn(2, self.min_heap)
        self.assertIn(3, self.min_heap)
        self.assertNotIn(4, self.min_heap)
        self.assertNotIn(5, self.min_heap)
        self.min_heap.pop()
        self.assertNotIn(1, self.min_heap)
        self.min_heap.pop()
        self.assertNotIn(2, self.min_heap)
        self.min_heap.pop()
        self.assertNotIn(3, self.min_heap)
