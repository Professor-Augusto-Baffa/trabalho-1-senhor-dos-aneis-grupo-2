import pygame
from pygame.locals import *
from copy import deepcopy

class Text:

    def __init__(self, text, pos, fontsize):
        self.text = text
        self.pos = pos

        self.fontname = None
        self.fontsize = fontsize
        self.fontcolor = Color('black')
        self.set_font()
        self.render()

    def set_font(self):
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        App.screen.blit(self.img, self.rect)

class App:

    def __init__(self):
        pygame.init()
        self.mapa = self.open_map()
        self.background_color = Color("ivory3")
        App.screen = pygame.display.set_mode((1200, 650))
        App.screen.fill(self.background_color)
        App.running = True
        pygame.display.set_caption("Jornada na Terra Media")

    def run(self):
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
            
            self.draw_map()

            pygame.display.update()

        pygame.quit()
    
    def open_map(self):
        map = open("mapa.txt",'r')
        matrix_map = []
        for line in map:
            matrix_line = []
            for letter in line:
                if letter != '\n':
                    matrix_line.append(letter)
            matrix_map.append(deepcopy(matrix_line))
        return matrix_map

    def draw_map(self):
        size = 5
        pos_x = 50
        pos_y = 50
        for line in self.mapa:
            for letter in line:
                if letter == '#':
                    pygame.draw.rect(self.screen, Color("blue4"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == '.':
                    pygame.draw.rect(self.screen, Color("chartreuse3"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'R':
                    pygame.draw.rect(self.screen, Color("cornsilk4"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'V':
                    pygame.draw.rect(self.screen, Color("darkgreen"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'M':
                    pygame.draw.rect(self.screen, Color("chocolate4"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'P':
                    pygame.draw.rect(self.screen, Color("black"), pygame.Rect(pos_x,pos_y,size,size))
                else:
                    pygame.draw.rect(self.screen, Color("darkgoldenrod1"), pygame.Rect(pos_x,pos_y,size,size))
                pos_x += size
            pos_y += size
            pos_x = 50


if __name__ == '__main__':
    App().run()