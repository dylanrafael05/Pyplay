import math
import random
import pygame
import threads
import abc
from threads import *

MAX_SPRITES = 500

class InvalidGameObjectError(Exception):
    pass

class GameObject(abc.ABC):

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.angle = 0
        self.size = 100
        self.color = (255, 255, 255, 255)
        self.shown = True

        self._on_start = []
        self._on_clone_start = []

        self._event_map = {}

        all_sprites.append(self)

        self._threads: list[threads.Thread] = []
        
        self._is_clone = False

        self._with = None

    def _clone_from(self, other: 'GameObject') -> None:
        self.x = other.x
        self.y = other.y
        self.angle = other.angle
        self.size = other.size
        self.color = other.color
        self.costume = other.costume

        if not other._is_clone:
            self._on_start = other._on_clone_start
            self._on_clone_start = []
        else:
            self._on_start = other._on_start
            self._on_clone_start = other._on_clone_start

        self._event_map = {}

        self._is_clone = True
    
    @property
    @abc.abstractmethod
    def image(self) -> pygame.surface.Surface:
        ...
    
    def _add_event(self, ev, f):
        if ev in self._event_map:
            self._event_map[ev].append(f)
        else:
            self._event_map[ev] = [f]

    def _draw(self, surf: pygame.surface.Surface):

        if not self.shown:
            return

        rot_img: pygame.surface.Surface = \
            pygame.transform.rotozoom(self.image, self.angle, self.size / 100)

        rot_img.fill(self.color, special_flags=pygame.BLEND_RGBA_MIN)

        surf.blit(
            rot_img,
            pygame.Vector2(
                self.x - rot_img.get_width() / 2, 
                self.y - rot_img.get_height() / 2
            )
        )
    
    def _events(self, ev):
        if (ev in self._event_map):
            return self._event_map[ev]
        return []
    
    def __enter__(self) -> 'GameObject':
        cth = threads._cur_thread()
        self._with = cth.spawner
        cth.spawner = self
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        threads._cur_thread().spawner = self._with
        self._with = None


class Sprite(GameObject):

    def __init__(self, *all_costumes: str) -> None:
        super().__init__()
        
        self.costume = 0
        self.shown = True

        self._all_costumes = Sprite._load_all_images(all_costumes)

    def _clone_from(self, other: 'Sprite') -> None:
        super()._clone_from(other)

        self.costume = other.costume
        self.shown = other.shown

        self._all_costumes = other._all_costumes

    @staticmethod
    def _load_all_images(filenames: list[str]) -> list[pygame.surface.Surface]:

        out = []

        for filename in filenames:
            out.append(pygame.image.load(filename))
        
        return out
    
    @property
    def image(self) -> pygame.surface.Surface:
        return self._all_costumes[self.costume] 


class Text(GameObject):

    def __init__(self, font: str = "comic-sans", size = 20) -> None:
        super().__init__()

        if pygame.font.get_init():
            pygame.font.init()

        self._font = pygame.font.Font(font, size)
        self._size = size

        self.text = ''

    def _clone_from(self, other: 'Text') -> None:
        super()._clone_from(other)

        self._font = other._font
        self._size = other._size

        self.text = other.text

    def image(self) -> pygame.Surface:
        return self._font.render(self.text, 1, '#ffffff', '#00000000')


def start(spr: GameObject = None):
    """
    Defines a script to be run when a sprite is spawned.
    """

    if spr is not None:

        def inner(f):
            f = script(f)
            spr._on_start.append(f)
            return f
        return inner

    else:

        def inner(f):
            f = script(f)
            all_starts.append(f)
            return f
        return inner

def clone_start(spr: GameObject):
    """
    Defines a script to be run when a sprite is spawned.
    """

    def inner(f):
        f = script(f)
        spr._on_clone_start.append(f)
        return f
    return inner

def clone(spr: GameObject = None):
    """
    Clones a sprite.
    """
    if len(all_sprites) > MAX_SPRITES:
        return None

    spr = spr or get_current_sprite()

    clone = Sprite()
    clone._clone_from(spr)

    for _cs in clone._on_start:
        threads.spawner = clone
        _cs()
    threads.spawner = None
    
    return clone

def delete(spr: GameObject = None):
    """
    Deletes a sprite.
    """
    spr = spr or get_current_sprite()
    all_sprites.remove(spr)
    
    for thread in spr._threads:
        thread.kill()

    threads.thread_kill_check()

def set_size(factor: int):
    ''' changes the size by a specific number'''
    get_current_sprite().size = factor

def change_size(factor: int):
    ''' changes the size by a specific number'''
    get_current_sprite().size += factor

def move(x: int, y: int):
    """
    Moves a sprite by a given amount.
    """
    spr = get_current_sprite()
    spr.x += x
    spr.y += y

def move_to(x: int, y: int):
    """
    Moves a sprite to a given position.
    """
    spr = get_current_sprite()
    spr.x = x
    spr.y = y

def move_x(x: int):
    """
    Moves a sprite by a given amount on the x axis.
    """
    get_current_sprite().x += x

def move_y(y: int):
    """
    Moves a sprite by a given amount on the y axis.
    """
    get_current_sprite().y += y

def rotate(angle: int):
    """
    Rotates a sprite by a given amount.
    """
    get_current_sprite().angle += angle

def rotate_to(angle: int):
    """
    Rotates a sprite to a given angle.
    """
    get_current_sprite().angle = angle

def go_to_random_position():
    """
    Moves a sprite to a random position on the screen.
    """
    spr = get_current_sprite()
    spr.x = random.randint(0, 1000)
    spr.y = random.randint(0, 666)

def glide_to_position(x: int, y: int, time: int):
    """
    Moves a sprite to a given position over a given time.
    """
    spr = get_current_sprite()

    xstart = spr.x
    ystart = spr.y

    xdiff = x - spr.x
    ydiff = y - spr.y

    frames = time * 60

    for i in range(frames):
        wait()
        spr.x = xstart + xdiff * (i / frames)
        spr.y = ystart + ydiff * (i / frames)

def move_forward(distance: int):
    """
    Moves a sprite forward by a given distance.
    """
    spr = get_current_sprite()

    spr.x += distance * math.cos(math.radians(spr.angle))
    spr.y += distance * math.sin(math.radians(spr.angle))

def move_backward(distance: int):
    """
    Moves a sprite backward by a given distance.
    """
    spr = get_current_sprite()

    spr.x -= distance * math.cos(math.radians(spr.angle))
    spr.y -= distance * math.sin(math.radians(spr.angle))

def turn_left(angle: int):
    """
    Turns a sprite left by a given angle.
    """
    spr = get_current_sprite()
    spr.angle -= angle

def turn_right(angle: int):
    """
    Turns a sprite right by a given angle.
    """
    spr = get_current_sprite()
    spr.angle += angle

def is_clone():
    """
    Get if the current sprite is a clone
    """
    return get_current_sprite()._is_clone

def change_color(r : int, g: int, b : int):
    """
    Change the color tint of this sprite
    """
    spr = get_current_sprite()
    color = (r, g, b, 255)
    spr.color = color

def ghost(alpha):
    """
    Change the ghost (alpha) of this sprite
    """
    spr = get_current_sprite()
    spr.color = spr.color[0:3] + (255 - (alpha/100)*255,)

def show():
    """
    Show this sprite
    """
    spr = get_current_sprite()
    spr.shown = True

def hide():
    """
    Hide this sprite
    """
    spr = get_current_sprite()
    spr.shown = False

def next_costume():
    """
    Switch this sprite to the next costume
    """
    spr = get_current_sprite()
    if not isinstance(spr, Sprite):
        raise InvalidGameObjectError('Cannot call next_costume with non-Sprite')
    spr.costume = (spr.costume + 1) % len(spr._all_costumes)

def set_text(txt: str):
    """
    Set the text of the given sprite
    """
    spr = get_current_sprite()
    if not isinstance(spr, Text):
        raise InvalidGameObjectError('Cannot call set_text with non-Text')
    spr.text = txt

    
all_sprites: list[Sprite] = []
all_starts: list[object] = []