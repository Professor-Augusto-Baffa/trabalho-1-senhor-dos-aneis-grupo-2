import pygame

from Button import Button

from pygame.locals import *
import map

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
        self.mapa = map.Map.read_from_file("mapa.txt")
        self.background_color = Color("ivory3")
        App.screen = pygame.display.set_mode((1200, 650))
        App.screen.fill(self.background_color)
        App.running = True
        pygame.display.set_caption("Jornada na Terra Media")
        self.tempo_total = 0
        self.jornada_string = "Tempo da jornada: {tempo}".format(tempo=self.tempo_total)
        self.timer = Text(self.jornada_string,(30,400),32)
        self.go_button = Button(700,400,150,80,"Iniciar",onclickFunction=self.foo, screen=App.screen)
        self.stop_button = Button(500,400,150,80,"Iniciar",onclickFunction=self.foo, screen=App.screen)
        self.reset_button = Button(300,400,150,80,"Iniciar",onclickFunction=self.foo, screen=App.screen)
        
    def run(self):
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
            #self.jornada_string = "Tempo da jornada: {tempo}".format(tempo=self.tempo_total)
            #self.timer = Text(self.jornada_string,(30,400),32)
            self.go_button.process()
            self.stop_button.process()
            self.reset_button.process()
            self.draw_map()
            self.timer.draw()
            pygame.display.update()

        pygame.quit()

    def draw_map(self):
        
        size = 5
        pos_x = 20
        pos_y = 20
        for line in self.mapa.matrix:
            for tile in line:
                letter = tile.terrain_type
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
            pos_x = 20

    def foo(self):
        self.tempo_total+=1
        print(self.tempo_total)

    def start_search(self):
        #TODO
        return

    def reset_search(self):
        #TODO
        return

    def stop_search(self):
        #TODO
        return

if __name__ == '__main__':
    App().run()