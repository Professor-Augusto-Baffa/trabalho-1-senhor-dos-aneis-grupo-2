from src.map import *

import unittest
from unittest.mock import patch, mock_open

class TileCreationTestCase(unittest.TestCase):

#'.RVMP#123456789ABCDEFGHI'

    def setUp(self) -> None:
        pass

    def test_tile_creation(self) -> None:
        types = [('.', 1), ('R', 5), ('V', 10), ('M', 200)]
        for t, c in types:
            tile = Tile(t)
            cost = tile.get_cost()
            self.assertEqual(cost, c, f'Wrong cost for tile "{t}". Expected "{c}", got "{cost}".')
        return

    def test_blocked_tile_creation(self) -> None:
        types = 'P#'
        for t in types:
            tile = Tile(t)
            cost = tile.get_cost()
            self.assertGreater(cost, 100_000, f'Bad cost for tile "{t}". Cost "{cost}" is less than 100 000.')
        return

    def test_event_tile_creation(self) -> None:
        for l in '123456789ABCDEFGHI':
            tile = Tile(l)
            cost = tile.get_cost()
            self.assertEqual(cost, 0, f'Wrong cost for event tile "{l}". Expected "0", got "{cost}".')

    def test_invalid_tile_creation(self) -> None:
        for l in '0JKLabf@!;':
            with self.assertRaises(ValueError, msg=f'Invalid tile "{l}" did not raise.') as cm:
                Tile(l)
        return
    
class MapCreationTestCase(unittest.TestCase):
    #   . V R #
    #   P M 1 #

    def setUp(self) -> None:
        self.test_matrix = [
            [Tile('.'), Tile('V'), Tile('R'), Tile('#')],
            [Tile('P'), Tile('M'), Tile('1'), Tile('#')]
        ]
        self.test_file_contents = '''.VR#
PM1#'''

    def test_map_creation(self):
        map = Map(self.test_matrix)
        self.assertEqual(map.n_cols, 4)
        self.assertEqual(map.n_lines, 2)
        for i in range(2):
            self.assertListEqual(self.test_matrix[i], map.matrix[i])
        return
    
    def test_map_creation_from_file(self):
        file_path = '/fake/path'
        with patch('src.map.open', new=mock_open(read_data=self.test_file_contents)) as _file:
            map = Map.read_from_file(file_path)
            self.assertEqual(map.n_cols, 4)
            self.assertEqual(map.n_lines, 2)
            for i in range(2):
                for j in range(4):
                    self.assertEqual(self.test_matrix[i][j].terrain_type, map.matrix[i][j].terrain_type)
                    self.assertEqual(self.test_matrix[i][j].get_cost(), map.matrix[i][j].get_cost())
            return
