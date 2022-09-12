from src.utils import MinHeap

import typing
from math import inf as infinity


W = typing.TypeVar('W')

class Node(typing.Generic[W]):
    """Node to be used for pathfinding.
    
    Stores an accumulated cost, a cost estimation, the previous node, and a wrapped value.
    """

    def __init__(self, element: W, cost: float, estimation: float) -> None:
        self.wrapped: W = element
        self.previous_node: typing.Optional[Node] = None
        self.accumulated_cost: float = cost
        self.estimated_cost: float = estimation
    
    def __repr__(self) -> str:
        prevWrapped = 'None'
        if self.previous_node is not None:
            prevWrapped = self.previous_node.wrapped.__repr__()
        return f'({self.wrapped}, {prevWrapped}, {self.accumulated_cost}, {self.estimated_cost})'


T = typing.TypeVar('T')

class SearchAgent(typing.Generic[T]):
    '''Implementation of a generic A* search algorithm.
    
    This implementation can be customized through dependency injection on the initializer.
    Note: The cost to reach the first element is always zero. The cost to reach any 
    neighbor of a given node N is equal to the cost of N returned by the cost function.
    '''

    def __init__(self,
            cost_function: typing.Callable[[T], float], 
            heuristic_function: typing.Callable[[T, T], float], 
            expansion_function: typing.Callable[[T], typing.List[T]]
        ) -> None:
        '''Create a SearchAgent
        
        Parameters
        ----------
        cost_function
            Function that returns the individual cost of one given element
        heuristic_function
            Function that estimates the cost of the path between two elements.
            This funtion should never overestimate the cost of a path.
        expansion_function
            Funtion that returns all nodes that can be reached for a given node (its neighbors)
        '''
        self.frontier: MinHeap[Node[T]] = MinHeap()
        self.get_cost = cost_function
        self.heuristic = heuristic_function
        self.expand_neighbors = expansion_function

    def _reconstruct_path(self, destination: Node[T]) -> typing.List[T]:
        path: typing.List[T] = [destination.wrapped]
        current = destination
        while current.previous_node is not None:
            current = current.previous_node
            path.append(current.wrapped)
        path.reverse()
        return path

    def find_path(self, origin: T, goal: T) -> typing.List[T]:
        wrapped_values: typing.Dict[T, Node[T]] = dict()
        start_heuristic = self.heuristic(origin, goal)
        start_node = Node(origin, 0, start_heuristic)
        wrapped_values[origin] = start_node
        self.frontier.push(start_node, start_node.estimated_cost)

        while not self.frontier.is_empty():
            current_node = self.frontier.pop()
            if current_node.wrapped == goal:
                return self._reconstruct_path(current_node)
            for new_neighbor in self.expand_neighbors(current_node.wrapped):
                # The cost of a path is sum {[origin, end)} (not including the end node)
                cost_from_here = current_node.accumulated_cost + self.get_cost(current_node.wrapped)
                new_neighbor_node = wrapped_values.get(new_neighbor, None)

                if new_neighbor_node is None:
                    # Create a new node with infinity as the accumulated cost
                    # The heuristic does not matter as it will be recalculated
                    new_neighbor_node = Node(new_neighbor, infinity, 0)
                    wrapped_values[new_neighbor] = new_neighbor_node

                if cost_from_here < new_neighbor_node.accumulated_cost:
                    # Found a better path
                    new_neighbor_node.accumulated_cost = cost_from_here
                    new_estimation = self.heuristic(new_neighbor, goal)
                    new_neighbor_node.estimated_cost = cost_from_here + new_estimation
                    new_neighbor_node.previous_node = current_node
                    if new_neighbor_node not in self.frontier:
                        self.frontier.push(new_neighbor_node, new_neighbor_node.estimated_cost)
                    else:
                        # Changed cost of existing node in heap
                        self.frontier.update_priority(new_neighbor_node, new_neighbor_node.estimated_cost)
                        self.frontier.reorganize()
        
        # Failed to reach goal
        return []



