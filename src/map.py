from copy import deepcopy
import typing

class Tile:

    VALID_TYPES = '.RVMP#123456789ABCDEFGHI'

    def __init__(self, letter: str) -> None:
        if letter not in Tile.VALID_TYPES:
            raise ValueError(f'Invalid character {letter}')
        self.terrain_type = letter
    
    def get_cost(self) -> float:
        if self.terrain_type == '.':
            return 1
        if self.terrain_type == 'R':
            return 5
        if self.terrain_type == 'V':
            return 10
        if self.terrain_type == 'M':
            return 200
        if self.terrain_type == 'P' or self.terrain_type == '#':
            return 1e30
        if self.terrain_type in Tile.VALID_TYPES:
            return 0
        raise ValueError(f'Invalid character {self.terrain_type}')

class Map:

    def __init__(self, matrix: typing.List[typing.List[Tile]]) -> None:
        self.matrix = matrix
        self.n_lines = len(matrix)
        if self.n_lines > 0:
            self.n_cols = len(matrix[0])
        else:
            self.n_cols = 0
        return

    @staticmethod
    def read_from_file(file_name: str) -> 'Map':
        matrix_map = []
        with open(file_name, 'r') as file:
            for line in file:
                matrix_line = []
                for letter in line:
                    if letter != '\n':
                        matrix_line.append(Tile(letter))
                matrix_map.append(deepcopy(matrix_line))
        
        return Map(matrix_map)