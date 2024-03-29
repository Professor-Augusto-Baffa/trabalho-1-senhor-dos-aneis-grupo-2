import map, display
import searchagent as search

import builtins
import pygame
from pygame.locals import *
import typing

class PathFinder:

    TileIndex = typing.Tuple[int, int]

    def __init__(
        self, map_: map.Map,
        updated_path: typing.Optional[typing.Callable[[str, str, typing.List[TileIndex]], None]] = None,
        found_best_path: typing.Optional[typing.Callable[[str, str, typing.List[TileIndex]], None]] = None,
        finished: typing.Optional[typing.Callable[[], None]] = None
    ) -> None:
        # Map
        self.map = map_
        # Callbacks
        self.updated_path = updated_path
        self.found_best_path = found_best_path
        self.did_finish = finished


        self.goals: str = '123456789ABCDEFGHI'
        self.search_agent = search.SearchAgent(
            cost_function = self.get_cost,
            heuristic_function = self.estimate_cost,
            expansion_function = self.get_neighbours
        )

        # Resetable
        self.paths: typing.Dict[typing.Tuple[str, str], typing.List['self.TileIndex']]
        self.did_start: bool
        self.is_done: bool
        self.current_goal_index: int
        self.generator: typing.Optional[typing.Generator[search.Node[self.TileIndex], None, typing.List[self.TileIndex]]]
        self.reset()

    def reset(self) -> None:
        self.paths = dict()
        self.did_start = False
        self.is_done = False
        self.current_goal_index = 1
        self.generator = None
        self.search_agent.reset()
    
    def _start(self) -> None:
        self.did_start = True
        self.current_goal_index = 1
    
    def _current_goal_is_done(self) -> bool:
        current_start = self.goals[self.current_goal_index - 1]
        current_goal = self.goals[self.current_goal_index]
        current_path = self.paths.get((current_start, current_goal), None)
        return current_path is not None

    def _start_next_goal(self) -> bool:
        if self.current_goal_index == len(self.goals) - 1:
            self._finish()
            return False
        if self._current_goal_is_done():
            # When the first goal is started, it won't be done yet
            self.current_goal_index += 1
        current_start = self.goals[self.current_goal_index - 1]
        current_goal = self.goals[self.current_goal_index]
        start_tile = self.map.get_event_tile(current_start)
        end_tile = self.map.get_event_tile(current_goal)
        self.generator = self.search_agent.get_best_path_generator(start_tile, end_tile)
        return True
    
    def _finish(self) -> None:
        # Set done
        self.is_done = True
        # Use callback
        if self.did_finish is None:
            return
        self.did_finish()

    def _found_best_path(self, path: typing.List[TileIndex]) -> None:
        # Remove generator
        self.generator = None
        # Update saved path
        current_start = self.goals[self.current_goal_index - 1]
        current_goal = self.goals[self.current_goal_index]
        self.paths[current_start, current_goal] = path
        self.search_agent.reset()
        # Use callback
        if self.found_best_path is None:
            return
        self.found_best_path(current_start, current_goal, path)

    def _update_ongoing_path(self, new_node: search.Node) -> None:
        # Update saved path
        path_to_current = self.search_agent.reconstruct_path(self.search_agent.current_node)
        new_path = path_to_current + [new_node.wrapped]
        current_start = self.goals[self.current_goal_index - 1]
        current_goal = self.goals[self.current_goal_index]
        self.paths[current_start, current_goal] = new_path
        # Use callback
        if self.updated_path is None:
            return
        self.updated_path(current_start, current_goal, new_path)


    def update(self) -> None:
        # Check if already done
        if self.is_done:
            return
        # Check if already started
        if not self.did_start:
            self._start()
        # Check if currently looking for a path
        if self.generator == None:
            pending_goal = self._start_next_goal()
            if not pending_goal:
                return
        # Try to get a new value
        try:
            last_visited_node = next(self.generator)
        except StopIteration as e:
            # Done
            found_path = e.value
            self._found_best_path(found_path)
            return
        # Visited a new node
        self._update_ongoing_path(last_visited_node)

    def get_path(self, start: str, end: str) -> typing.Optional[typing.List[TileIndex]]:
        return self.paths.get((start, end), None)

    def get_accumulated_cost(self) -> float:
        return sum((self.get_section_cost(self.goals[i-1], self.goals[i]) for i in range(1, len(self.goals))))

    def get_section_cost(self, start: str, end: str) -> float:
        path = self.paths.get((start, end), None)
        if path is None:
            return 0
        return sum(builtins.map(lambda tile_index: self.get_cost(tile_index), path))

    # Search Agent methods
    
    def get_cost(self, tile: TileIndex) -> float:
        return self.map.get_tile(tile).get_cost()

    def estimate_cost(self, start: TileIndex, end: TileIndex) -> float:
        if start == end: return 0
        return (end[0] - start[0]) + (end[1] - start[1]) + self.get_cost(start) - 1

    def get_neighbours(self, tile: TileIndex) -> typing.List[TileIndex]:
        l = []
        # Up
        if tile[0] > 0: l.append( (tile[0] - 1, tile[1]) )
        # Left
        if tile[1] > 1: l.append( (tile[0], tile[1] - 1) )
        # Right
        if tile[1] < self.map.n_cols - 1: l.append( (tile[0], tile[1] + 1) )
        # Down
        if tile[0] < self.map.n_lines - 1: l.append( (tile[0] + 1, tile[1]) )
        return l


class App:

    def __init__(self):
        pygame.init()
        
        self.mapa = map.Map.read_from_file("mapa.txt")

        self.running = True

        self.speed: float = 180 # Melhor entre 0.1 e 200

        self.window = display.Window()
        self.window.add_event_handler('main_quit_handler', pygame.QUIT, lambda e: self.stop_running())

        button_height = 34
        button_v_pos = self.window.height - 20 - button_height

        timer_font_size = 32
        timer_height = timer_font_size + 10
        timer_v_pos = button_v_pos - 10 - timer_height

        map_v_pos = 10
        map_height = timer_v_pos - 20
        map_width = self.window.width - 2 * 10

        self.mapDisplay = display.MapDisplay(self.mapa, (10, map_v_pos), (map_width, map_height))
        self.mapDisplay.set_window(self.window)

        self.tempo_total = 0
        self.jornada_string = "Tempo da jornada: "
        self.timer = display.Text(self.jornada_string + str(self.tempo_total), (30, timer_v_pos), timer_font_size)
        self.timer.set_window(self.window)

        self.go_button = display.Button('Iniciar', (25, button_v_pos), (100, button_height), on_click=self.start_search)
        self.go_button.set_window(self.window)

        self.stop_button = display.Button('Parar', (150, button_v_pos), (100, button_height), on_click=self.stop_search)
        self.stop_button.set_window(self.window)

        self.step_button = display.Button('Step', (275, button_v_pos), (100, button_height), on_click=self.step_search)
        self.step_button.set_window(self.window)

        self.reset_button = display.Button('Zerar', (400, button_v_pos), (100, button_height), on_click=self.reset_search)
        self.reset_button.set_window(self.window)

        self.print_button = display.Button('Print path', (525, button_v_pos), (150, button_height), on_click=self.print_path)
        self.print_button.set_window(self.window)

        self.path_finder = PathFinder(
            self.mapa, updated_path=self.path_finder_updated_path, found_best_path=self.path_finder_found_best_path,
            finished=self.path_finder_finished_running
        )

        self.path_displays: typing.Dict[typing.Tuple[str, str], display.PathDisplay] = dict()
        self.tempo_total = 0
        self.frame_count = 0
        self.is_path_finder_running = False
        self.is_done = False
        
    def stop_running(self):
        print('Quit')
        self.running = False

    def reset(self):
        self.tempo_total = 0
        self.frame_count = 0
        self.is_path_finder_running = False
        self.is_done = False
        for display in self.path_displays.values():
            display.remove_from_window(self.window)
        self.path_displays.clear()
        self.path_finder.reset()

    def update_time_text(self):
        self.tempo_total = self.path_finder.get_accumulated_cost()
        self.timer.text = self.jornada_string + str(self.tempo_total)
    
    ###############
    # Path Finder #
    ###############

    def path_finder_updated_path(self, start: str, end: str, path: typing.List[PathFinder.TileIndex]) -> None:
        path_display = self.path_displays.get((start, end), None)
        if path_display is not None:
            path_display.path = path
            return
        path_display = display.PathDisplay(self.mapa, self.mapDisplay.pos, self.mapDisplay.size, path)
        path_display.set_window(self.window)
        self.path_displays[start, end] = path_display

    def path_finder_found_best_path(self, start: str, end: str, path: typing.List[PathFinder.TileIndex]) -> None:
        old_display = self.path_displays.get((start, end), None)
        if old_display is not None:
            self.window.remove_renderer(old_display._renderer_key)
        path_display = display.PathDisplay(self.mapa, self.mapDisplay.pos, self.mapDisplay.size, path, is_done=True)
        path_display.set_window(self.window)
        self.path_displays[start, end] = path_display

    def path_finder_finished_running(self) -> None:
        self.is_path_finder_running = False

    def run(self):
        while self.running:
            if self.is_path_finder_running:
                self.frame_count += 1
                if self.speed < 1.0:
                    n = int(1.0 / self.speed)
                    if self.frame_count % n == 0:
                        self.path_finder.update()
                else:
                    n = int(self.speed)
                    for _ in range(n):
                        if not self.is_path_finder_running:
                            break
                        self.path_finder.update()
            self.update_time_text()
            self.window.process_events()
            self.window.display()
        pygame.quit()

    def print_path(self):
        current_start = self.path_finder.map.get_event_tile(self.path_finder.goals[self.path_finder.current_goal_index - 1])
        current_goal = self.path_finder.map.get_event_tile(self.path_finder.goals[self.path_finder.current_goal_index])
        current_end_node = self.path_finder.search_agent.possible_next_node
        current_end = current_end_node.wrapped
        print('Goal: ', current_goal)
        print('Start: ', current_start)
        print('End: ', current_end)
        next_node = self.path_finder.search_agent.possible_next_node
        path = self.path_finder.search_agent.reconstruct_path(next_node)
        print('Path: ', path)


    def start_search(self):
        self.is_path_finder_running = True
        return

    def reset_search(self):
        self.reset()

    def stop_search(self):
        self.is_path_finder_running = False
        return
    
    def step_search(self):
        if self.is_path_finder_running:
            return
        if self.is_done:
            return
        self.path_finder.update()

if __name__ == '__main__':
    app = App()
    app.run()