import enum
import typing
import pygame
import map

class Window:

    RendererType = typing.Callable[[pygame.Surface], None]
    EventHandlerType = typing.Callable[[pygame.event.Event], None]

    def __init__(self) -> None:
        self.background_color = pygame.Color("ivory3")
        self.surface = pygame.display.set_mode((1200, 650))
        pygame.display.set_caption("Jornada na Terra Media")
        self.renderers: typing.Dict[str, 'Window.RendererType'] = dict()
        self.event_handlers: typing.Dict[int, typing.Dict[str, 'Window.RendererType']] = dict()
    
    def display(self) -> None:
        self.surface.fill(self.background_color)
        for render in self.renderers.values():
            render(self.surface)
        pygame.display.update()

    def add_renderer(self, key: str, renderer: 'Window.RendererType') -> None:
        self.renderers[key] = renderer
    
    def remove_renderer(self, key: str) -> None:
        del self.renderers[key]

    def add_event_handler(self, event_type: int, key: str, handler: 'Window.EventHandlerType') -> None:
        handlers = self.event_handlers.get(event_type, None)
        if handlers is None:
            handlers = dict()
            self.event_handlers[event_type] = handlers
        handlers[key] = handler
    
    def remove_event_handler(self, event_type: int, key: str) -> None:
        handlers = self.event_handlers.get(event_type, None)
        if handlers is None:
            return
        del handlers[key]
        if len(handlers.keys) > 0:
            return
        del self.event_handlers[event_type]
    
    def process_events(self):
        for event in pygame.event.get():
            handlers = self.event_handlers.get(event.type, None)
            if handlers is None:
                continue
            for handle in handlers.values():
                handle(event)
        return



class Rendered:
    '''Base class for elements that are drawn to the screen'''

    __instance_seq = 0

    def __init__(self) -> None:
        self._renderer_key = f'{Rendered}.{Rendered.__instance_seq}'
        Rendered.__instance_seq += 1
    
    def set_window(self, window: Window) -> None:
        window.add_renderer(self._renderer_key, self.draw)
    
    def draw(self, surface: pygame.Surface) -> None:
        '''Override to draw this element on the given surface'''
        pass
        


class Text(Rendered):

    def __init__(self, text: str, pos: typing.Tuple[int, int], fontsize: int):
        super().__init__()
        self.text = text
        self.pos = pos

        self.fontname: typing.Optional[str] = None
        self.fontsize = fontsize
        self.fontcolor = pygame.Color('black')
        self.set_font()

    def set_font(self) -> None:
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def draw(self, surface: pygame.Surface) -> None:
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos
        surface.blit(self.img, self.rect)



class ButtonState(enum.IntEnum):
    NORMAL = enum.auto()
    HIGHLIGHTED = enum.auto()
    PRESSED = enum.auto()



class Button(Rendered):

    def __init__(
        self, text: str, pos: typing.Tuple[int, int], size: typing.Tuple[int, int], 
        on_click: typing.Optional[typing.Callable[[], None]] = None
    ) -> None:
        super().__init__()

        self.text = text
        self.pos = pos
        self.size = size
        self.on_click = on_click
        self.state = ButtonState.NORMAL
        
        self.font = pygame.font.SysFont('Arial', 20)
        self.fontcolor = pygame.Color(20, 20, 20)
        self.fillColors: typing.Dict[ButtonState, str] = {
            ButtonState.NORMAL: '#ffffff',
            ButtonState.HIGHLIGHTED: '#666666',
            ButtonState.PRESSED: '#333333',
        }

        self.buttonSurface = pygame.Surface(size)
        self.buttonRect = pygame.Rect(self.pos, self.size)

        self.alreadyPressed = False
    
    def _is_mouse_down(self) -> bool:
        return pygame.mouse.get_pressed()[0]

    def _process_button_down(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        mouse_pos = pygame.mouse.get_pos()
        if not self.buttonRect.collidepoint(mouse_pos):
            self.state = ButtonState.NORMAL
            return
        # Mouse is inside button
        self.state = ButtonState.PRESSED
    
    def _process_button_up(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONUP:
            return
        mouse_pos = pygame.mouse.get_pos()
        if not self.buttonRect.collidepoint(mouse_pos):
            self.state = ButtonState.NORMAL
            return
        # Mouse is inside button
        self.on_click()
        self.state = ButtonState.HIGHLIGHTED
    
    def _process_mouse_move(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEMOTION:
            return
        mouse_pos = pygame.mouse.get_pos()
        if not self.buttonRect.collidepoint(mouse_pos):
            # Outside button
            self.state = ButtonState.NORMAL
            return
        # Mouse is inside button
        if self._is_mouse_down():
            self.state = ButtonState.PRESSED
        else:
            self.state = ButtonState.HIGHLIGHTED
    
    def set_window(self, window: Window) -> None:
        super().set_window(window)
        window.add_event_handler(pygame.MOUSEBUTTONDOWN, self._renderer_key, self._process_button_down)
        window.add_event_handler(pygame.MOUSEBUTTONUP, self._renderer_key, self._process_button_up)
        window.add_event_handler(pygame.MOUSEMOTION, self._renderer_key, self._process_mouse_move)

    def draw(self, surface: pygame.Surface) -> None:
        # Get bg color
        bg = self.fillColors.get(self.state, 'ff0000')
        # Get text surface
        img = self.font.render(self.text, True, self.fontcolor, bg)
        # Calculate position to center text on button
        text_size = img.get_size()
        dx = (self.size[0] - text_size[0]) / 2
        dy = (self.size[1] - text_size[1]) / 2
        text_pos = (self.pos[0] + dx, self.pos[1] + dy)
        pygame.draw.rect(surface, bg, self.buttonRect, border_radius=8)
        surface.blit(img, text_pos)



class MapDisplay(Rendered):

    def __init__(self, _map: map.Map) -> None:
        super().__init__()
        self.map = _map
    
    def draw(self, surface: pygame.Surface) -> None:
        size = 5
        pos_x = 20
        pos_y = 20
        for line in self.map.matrix:
            for tile in line:
                letter = tile.terrain_type
                if letter == '#':
                    pygame.draw.rect(surface, pygame.Color("blue4"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == '.':
                    pygame.draw.rect(surface, pygame.Color("chartreuse3"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'R':
                    pygame.draw.rect(surface, pygame.Color("cornsilk4"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'V':
                    pygame.draw.rect(surface, pygame.Color("darkgreen"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'M':
                    pygame.draw.rect(surface, pygame.Color("chocolate4"), pygame.Rect(pos_x,pos_y,size,size))
                elif letter == 'P':
                    pygame.draw.rect(surface, pygame.Color("black"), pygame.Rect(pos_x,pos_y,size,size))
                else:
                    pygame.draw.rect(surface, pygame.Color("darkgoldenrod1"), pygame.Rect(pos_x,pos_y,size,size))
                pos_x += size
            pos_y += size
            pos_x = 20
