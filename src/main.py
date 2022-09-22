import pygame
from pygame.locals import *

import map, display

class App:

    def __init__(self):
        pygame.init()
        
        self.mapa = map.Map.read_from_file("mapa.txt")

        self.running = True

        self.window = display.Window()
        self.window.add_event_handler(pygame.QUIT, 'main_quit_handler', lambda e: self.stop_running())

        self.mapDisplay = display.MapDisplay(self.mapa)
        self.mapDisplay.set_window(self.window)

        self.tempo_total = 0
        self.jornada_string = "Tempo da jornada: {tempo}".format(tempo=self.tempo_total)
        self.timer = display.Text(self.jornada_string, (30, 400), 32)
        self.timer.set_window(self.window)

        self.go_button = display.Button('Iniciar', (700, 400), (100, 60), on_click=self.start_search)
        self.go_button.set_window(self.window)

        self.stop_button = display.Button('Parar', (500, 400), (100, 60), on_click=self.stop_search)
        self.stop_button.set_window(self.window)

        self.reset_button = display.Button('Zerar', (300, 400), (100, 60), on_click=self.reset_search)
        self.reset_button.set_window(self.window)
        
    def stop_running(self):
        print('Quit')
        self.running = False

    def run(self):
        while self.running:
            self.window.process_events()
            self.window.display()
        pygame.quit()

    def start_search(self):
        #TODO
        print('START')
        return

    def reset_search(self):
        #TODO
        print('RESET')
        return

    def stop_search(self):
        #TODO
        print('STOP')
        return

if __name__ == '__main__':
    App().run()