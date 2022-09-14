from src.searchagent import *

import unittest
import typing

class NodeMinHeapTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(NodeMinHeapTestCase, self).__init__(*args, **kwargs)
        self.min_heap: typing.Optional[MinHeap[Node]]

    def setUp(self) -> None:
        self.min_heap = MinHeap()
        self.min_heap.push(Node('A', 0, 1), 1)
        self.min_heap.push(Node('B', 0, 2), 2)
        self.min_heap.push(Node('D', 0, 4), 4)

    def test_pop_order(self):
        self.assertFalse(self.min_heap.is_empty())
        self.assertEqual(self.min_heap.pop().wrapped, 'A')
        self.assertEqual(self.min_heap.pop().wrapped, 'B')
        self.assertEqual(self.min_heap.pop().wrapped, 'D')
        self.assertTrue(self.min_heap.is_empty())
    
    def test_add_remove(self):
        self.assertFalse(self.min_heap.is_empty())
        self.assertEqual(self.min_heap.pop().wrapped, 'A')
        self.min_heap.push(Node('C', 0, 3), 3)
        self.assertEqual(self.min_heap.pop().wrapped, 'B')
        self.assertEqual(self.min_heap.pop().wrapped, 'C')
        self.min_heap.push(Node('C', 0, 3), 3)
        self.assertEqual(self.min_heap.pop().wrapped, 'C')
        self.assertEqual(self.min_heap.pop().wrapped, 'D')
        self.assertTrue(self.min_heap.is_empty())
    
WrappedType = typing.Tuple[int, int]

class SearchAgentTestCase(unittest.TestCase):
    """Test the search agent in a fixed scenario"""
    # 1  1  1  2  3
    # 3  5  1  2  1
    # 10 2  1  2  3
    # 15 1  20 4  4
    # 1  3  2  5  0

    def __init__(self, *args, **kwargs):
        super(SearchAgentTestCase, self).__init__(*args, **kwargs)
        self.search_agent: typing.Optional[SearchAgent[WrappedType]]
        self.board = typing.Optional[typing.Dict[WrappedType, int]]
    
    def setUp(self) -> None:
        self.board = {
            (1, 1): 1,  (1, 2): 1,  (1, 3): 1,  (1, 4): 2,  (1, 5): 3,
            (2, 1): 3,  (2, 2): 5,  (2, 3): 1,  (2, 4): 2,  (2, 5): 1,
            (3, 1): 10, (3, 2): 2,  (3, 3): 1,  (3, 4): 2,  (3, 5): 3,
            (4, 1): 15, (4, 2): 1,  (4, 3): 20, (4, 4): 4,  (4, 5): 15,
            (5, 1): 1,  (5, 2): 2,  (5, 3): 2,  (5, 4): 5,  (5, 5): 0
        }
        def cost_f(case: WrappedType) -> float:
            return self.board[case]
        def h_f(start: WrappedType, end: WrappedType) -> float:
            return (end[0] - start[0]) + (end[1] - start[1]) + cost_f(start) - 1
        def exp_f(case: WrappedType) -> typing.List[WrappedType]:
            l = []
            if case[0] > 1: l.append( (case[0] - 1, case[1]) )
            if case[0] < 5: l.append( (case[0] + 1, case[1]) )
            if case[1] > 1: l.append( (case[0], case[1] - 1) )
            if case[1] < 5: l.append( (case[0], case[1] + 1) )
            return l
        self.search_agent = SearchAgent(cost_f, h_f, exp_f)

    def test_path_finding(self) -> None:
        correct_path: typing.List[WrappedType] = [
            (1,1), (1,2), (1,3), (2,3), (3,3), (3,4), (4,4), (5,4), (5,5)
        ]
        path_gen = self.search_agent._find_path((1, 1), (5, 5), interactive=False)
        with self.assertRaises(StopIteration) as context_manager:
            next(path_gen)
        path = context_manager.exception.value
        self.assertListEqual(path, correct_path)

    def test_get_best_path(self) -> None:
        correct_path: typing.List[WrappedType] = [
            (1,1), (1,2), (1,3), (2,3), (3,3), (3,4), (4,4), (5,4), (5,5)
        ]
        path = self.search_agent.get_best_path((1, 1), (5, 5))
        self.assertListEqual(path, correct_path)
    
    def test_get_best_path_alternative_1(self) -> None:
        self.board[4, 4] = 7
        correct_path: typing.List[WrappedType] = [
            (1,1), (1,2), (1,3), (2,3), (3,3), (3,2), (4,2), (5,2), (5,3), (5,4), (5,5)
        ]
        path = self.search_agent.get_best_path((1, 1), (5, 5))
        self.assertListEqual(path, correct_path)
    
    def test_get_best_path_alternative_2(self) -> None:
        self.board[4, 4] = 7
        self.board[4, 5] = 4
        correct_path: typing.List[WrappedType] = [
            (1,1), (1,2), (1,3), (2,3), (3,3), (3,4), (3,5), (4,5), (5,5)
        ]
        path = self.search_agent.get_best_path((1, 1), (5, 5))
        self.assertListEqual(path, correct_path)

class InteractiveSearchAgentTestCase(unittest.TestCase):
    # 1  3
    # 2  0

    def __init__(self, *args, **kwargs):
        super(InteractiveSearchAgentTestCase, self).__init__(*args, **kwargs)
        self.search_agent: typing.Optional[SearchAgent[WrappedType]]
        self.board = typing.Optional[typing.Dict[WrappedType, int]]
    
    def setUp(self) -> None:
        self.board = {
            (1, 1): 1,  (1, 2): 3,
            (2, 1): 2,  (2, 2): 0
        }
        def cost_f(case: WrappedType) -> float:
            return self.board[case]
        def h_f(start: WrappedType, end: WrappedType) -> float:
            if start == end: return 0
            return (end[0] - start[0]) + (end[1] - start[1]) + cost_f(start) - 1
        def exp_f(case: WrappedType) -> typing.List[WrappedType]:
            l = []
            # Up
            if case[0] == 2: l.append( (case[0] - 1, case[1]) )
            # Left
            if case[1] == 2: l.append( (case[0], case[1] - 1) )
            # Right
            if case[1] == 1: l.append( (case[0], case[1] + 1) )
            # Down
            if case[0] == 1: l.append( (case[0] + 1, case[1]) )
            return l
        self.search_agent = SearchAgent(cost_f, h_f, exp_f)

    def test_interactive_path_finding(self) -> None:
        path_generator = self.search_agent.get_best_path_generator((1, 1), (2, 2))
        # Current = (1, 1)
        self.assertEqual(next(path_generator).wrapped, (1, 2))
        self.assertEqual(self.search_agent.current_node.wrapped, (1, 1))
        self.assertEqual(next(path_generator).wrapped, (2, 1))
        # Current = (2, 1)
        self.assertEqual(next(path_generator).wrapped, (1, 1))
        self.assertEqual(self.search_agent.current_node.wrapped, (2, 1))
        self.assertEqual(next(path_generator).wrapped, (2, 2))
        # Current = (2, 2)
        with self.assertRaises(StopIteration) as cm:
            next(path_generator)
        self.assertEqual(self.search_agent.current_node.wrapped, (2, 2))
        final_list = cm.exception.value
        self.assertListEqual(final_list, [(1, 1), (2, 1), (2, 2)])
