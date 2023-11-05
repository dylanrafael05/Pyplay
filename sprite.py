import math
import random
import pygame
import threads
import basics
import abc
from threads import *
from worldtransform import *

MAX_SPRITES = 500

class InvalidGameObjectError(Exception):
    pass

class GameObject(abc.ABC):

    _starts: dict[type['GameObject'], list[object]] = {}
    _clone_starts: dict[type['GameObject'], list[object]] = {}
    _draws: dict[type['GameObject'], list[object]] = {}

    @classmethod
    def define_start(cls, f):
        if cls not in cls._starts:
            cls._starts[cls] = []
        cls._starts[cls].append(f)
    @classmethod
    def define_clone_start(cls, f):
        if cls not in cls._clone_starts:
            cls._starts[cls] = []
        cls._clone_starts[cls].append(f)
    @classmethod
    def define_draw(cls, f):
        if cls not in cls._draws:
            cls._starts[cls] = []
        cls._draws[cls].append(f)

    @classmethod 
    def _get_starts(cls):
        if cls not in cls._starts:
            return []
        return cls._starts[cls] + (cls.__base__._get_starts() if issubclass(cls.__base__, GameObject) else [])
    @classmethod 
    def _get_clone_starts(cls):
        if cls not in cls._clone_starts:
            return []
        return cls._clone_starts[cls] + (cls.__base__._get_clone_starts() if issubclass(cls.__base__, GameObject) else [])
    @classmethod 
    def _get_draws(cls):
        if cls not in cls._draws:
            return []
        return cls._draws[cls] + (cls.__base__.get_draws() if issubclass(cls.__base__, GameObject) else [])

    @property
    def pos(self) -> pygame.Vector2:
        return ScreenToWorld(pygame.Vector2(self._x_scr, self._y_scr))

    @pos.setter
    def pos(self, val: pygame.Vector2):
        val = WorldToScreen(val)
        self._x_scr = val.x
        self._y_scr = val.y

    def __init__(self) -> None:
        self.angle = 0
        self.size = 100
        self.color = (255, 255, 255, 255)
        self.shown = True
        
        self._x_scr = 0
        self._y_scr = 0

        self._on_start = self.__class__._get_starts()
        self._on_clone_start = self.__class__._get_clone_starts()
        self._on_draw = self.__class__._get_draws()

        self._event_map = {}

        self._threads: list[threads.PyplayThread] = []
        
        self._is_clone = False

        self._with = None

        self._lock = threading.Lock()
        
        _all_objects.append(self)

        self.dead = False

        if basics.running():
            self._begin()

    def _clone_from(self, other: 'GameObject') -> None:
        self._x_scr = other._x_scr
        self._y_scr = other._y_scr
        self.angle = other.angle
        self.size = other.size
        self.color = other.color
        self.costume = other.costume

        if not other._is_clone:
            self._on_start = other._on_clone_start
            self._on_clone_start = []
            self._on_draw = other._on_draw
        else:
            self._on_start = other._on_start
            self._on_clone_start = other._on_clone_start
            self._on_draw = other._on_draw

        self._event_map = {}

        self._is_clone = True

    def _begin(self):
        for os in self._on_start:
            threads.spawner = self
            os()
        threads.spawner = None
    
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
                self._x_scr - rot_img.get_width() / 2, 
                self._y_scr - rot_img.get_height() / 2
            )
        )

        for draw in self._on_draw:
            draw()
    
    def _events(self, ev):
        if (ev in self._event_map):
            return self._event_map[ev]
        return []
        
    def _aabb_screen(self):
        """
        Returns the axis-aligned bounding box of the sprite in screen coordinates.
        
        (x, y, width, height)
        """
        img = self.image
        return pygame.Rect(
            self._x_scr - (img.get_width() / 2) * self.size / 100,
            self._y_scr - (img.get_height() / 2) * self.size / 100,
            img.get_width() * self.size / 100,
            img.get_height() * self.size / 100
        )
    def _set_angle(self, angle):
        if (angle < 0):
            angle += 360
        self.angle = angle

    def __enter__(self) -> 'GameObject':
        self._with = maybe_this()
        assign_this_unsafe(self)
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        assign_this_unsafe(self._with)
        self._with = None


class Sprite(GameObject):

    def __init__(self, *all_costumes: str) -> None:
        
        self.costume = 0
        self.shown = True

        self._all_costumes = Sprite._load_all_images(all_costumes)

        super().__init__()

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
        
        if not pygame.font.get_init():
            pygame.font.init()

        self._font = pygame.font.SysFont(font, size)
        self._size = size

        self.text = ''

        super().__init__()

    def _clone_from(self, other: 'Text') -> None:
        super()._clone_from(other)

        self._font = other._font
        self._size = other._size

        self.text = other.text

    @property
    def image(self) -> pygame.Surface:
        return self._font.render(self.text, 1, '#ffffff')

def on_draw(spr: GameObject | type[GameObject]):
    """
    Defines a script to be run when a sprite is drawn.
    """

    if isinstance(spr, type):

        def inner(f):
            f = script(f)
            spr.define_draw(f)
            return f
        return inner
    
    else:

        def inner(f):
            f = script(f)
            spr._on_draw.append(f)
            return f
        return inner

def start(spr: GameObject | type[GameObject] = None):
    """
    Defines a script to be run when a sprite is spawned.
    """

    if isinstance(spr, type):

        def inner(f):
            f = script(f)
            spr.define_start(f)
            return f
        return inner

    elif spr is not None:

        def inner(f):
            f = script(f)
            spr._on_start.append(f)
            return f
        return inner

    else:

        def inner(f):
            f = script(f)
            _all_starts.append(f)
            return f
        return inner

def clone_start(spr: GameObject | type[GameObject]):
    """
    Defines a script to be run when a sprite is spawned.
    """
    if isinstance(spr, type):

        def inner(f):
            f = script(f)
            spr.define_clone_start(f)
            return f
        return inner
    
    else:

        def inner(f):
            f = script(f)
            spr._on_clone_start.append(f)
            return f
        return inner


def clone(spr: GameObject = None):
    """
    Clones a sprite.
    """
    if len(_all_objects) > MAX_SPRITES:
        return None

    spr = spr or this()

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
    spr = spr or this()
    _all_objects.remove(spr)
    
    for thread in list(spr._threads):
        thread.mark_kill()

    spr.dead = True

    threads.thread_kill_check()

def set_size(factor: int):
    ''' changes the size by a specific number'''
    this().size = factor

def change_size(factor: int):
    ''' changes the size by a specific number'''
    this().size += factor

def move(x: int, y: int):
    """
    Moves a sprite by a given amount.
    """
    spr = this()
    spr.pos += pygame.Vector2(x, y)

def move_to_other(other: GameObject):
    """
    Moves a sprite to a given position.
    """
    spr = this()
    spr.pos = other.pos

def move_to(x: int, y: int):
    """
    Moves a sprite to a given position.
    """
    spr = this()
    spr.pos = pygame.Vector2(x, y)

def move_x(x: int):
    """
    Moves a sprite by a given amount on the x axis.
    """
    this()._x_scr += WorldToScreenFactorX(x)

def move_y(y: int):
    """
    Moves a sprite by a given amount on the y axis.
    """
    this()._y_scr += WorldToScreenFactorY(y)

def rotate(angle: int):
    """
    Rotates a sprite by a given amount.
    """
    this().angle += angle

def rotate_to(angle: int):
    """
    Rotates a sprite to a given angle.
    """
    this().angle = angle

def go_to_random_position():
    """
    Moves a sprite to a random position on the screen.
    """
    spr = this()
    spr._x_scr = random.randint(0, SCREEN_DIMS.x)
    spr._y_scr = random.randint(0, SCREEN_DIMS.y)

def glide_to_position(x: int, y: int, time: int):
    """
    Moves a sprite to a given position over a given time.
    """
    spr = this()

    x, y = WorldToScreen(pygame.Vector2(x, y))

    xstart = spr._x_scr
    ystart = spr._y_scr

    xdiff = x - spr._x_scr
    ydiff = y - spr._y_scr

    start = basics.timer_since_start()

    while basics.timer_since_start() - start < time:
        wait()
        spr._x_scr = xstart + xdiff * ((basics.timer_since_start() - start) / time)
        spr._y_scr = ystart + ydiff * ((basics.timer_since_start() - start) / time)

    spr._x_scr = x
    spr._y_scr = y

def move_forward(distance: int):
    """
    Moves a sprite forward by a given distance.
    """
    spr = this()

    spr._x_scr += distance * math.cos(math.radians(spr.angle))
    spr._y_scr += distance * math.sin(math.radians(spr.angle))

def move_backward(distance: int):
    """
    Moves a sprite backward by a given distance.
    """
    spr = this()

    spr._x_scr -= distance * math.cos(math.radians(spr.angle))
    spr._y_scr -= distance * math.sin(math.radians(spr.angle))

def turn_left(angle: int):
    """
    Turns a sprite left by a given angle.
    """
    spr = this()
    spr.angle -= angle

def turn_right(angle: int):
    """
    Turns a sprite right by a given angle.
    """
    spr = this()
    spr.angle += angle

def is_clone():
    """
    Get if the current sprite is a clone
    """
    return this()._is_clone

def change_color(r : int, g: int, b : int):
    """
    Change the color tint of this sprite
    """
    spr = this()
    color = (r, g, b, 255)
    spr.color = color

def ghost(alpha):
    """
    Change the ghost (alpha) of this sprite
    """
    spr = this()
    spr.color = spr.color[0:3] + (255 - (alpha/100)*255,)

def show():
    """
    Show this sprite
    """
    spr = this()
    spr.shown = True

def hide():
    """
    Hide this sprite
    """
    spr = this()
    spr.shown = False

def is_touching(spr: Sprite):
    """
    Returns if the current sprite is touching another sprite.
    """
    spr1 = this()._aabb_screen()
    spr2 = spr._aabb_screen()

    return spr1.colliderect(spr2)

def is_touching_edge():
    """
    Returns if the current sprite is touching the edge of the screen.
    """
    spr = this()._aabb_screen()

    return spr[0] < 0 or spr[0] + spr[2] > SCREEN_DIMS.x or \
        spr[1] < 0 or spr[1] + spr[3] > SCREEN_DIMS.y


def bounce_if_on_edge():
    """
    Bounces the sprite if it is touching the edge of the screen.
    """
    spr = this()
    spr_aabb = spr._aabb_screen()

    print(spr.angle)

    width, height = pygame.display.get_surface().get_size()

    if spr_aabb[0] - spr_aabb[2] / 2 < 0:
        spr._x_scr = (spr_aabb[2] / 2) * 2
        spr.angle = 180 - spr.angle
    elif spr_aabb[0] + spr_aabb[2] / 2 > width:
        spr._x_scr = width - (spr_aabb[2] / 2) * 2
        spr.angle = 180 - spr.angle
    if spr_aabb[1] - spr_aabb[3] / 2 < 0:
        spr._y_scr = (spr_aabb[3] / 2) * 2
        spr.angle = 360 - spr.angle
    elif spr_aabb[1] + spr_aabb[3] / 2 > height:
        spr._y_scr = height - (spr_aabb[3] / 2) * 2
        spr.angle = 360 - spr.angle
    
    if (spr.angle < 0):
        spr.angle += 360
    spr.angle %= 360

def next_costume():
    """
    Switch this sprite to the next costume
    """
    spr = this()
    if not isinstance(spr, Sprite):
        raise InvalidGameObjectError('Cannot call next_costume with non-Sprite')
    spr.costume = (spr.costume + 1) % len(spr._all_costumes)

def set_text(*args):
    """
    Set the text of the given sprite
    """
    spr = this()
    if not isinstance(spr, Text):
        raise InvalidGameObjectError('Cannot call set_text with non-Text')
    spr.text = ' '.join(str(x) for x in args)


def this() -> GameObject:
    return threads.this()


class SayText(Text):

    def __init__(self, follow: GameObject, life: float, font: str = "comic-sans", size=20) -> None:
        self.follow = follow
        self.life = life
        super().__init__(font, size)

    def _draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, '#ffffff', self._aabb_screen().inflate(10, 10), border_radius=10)
        super()._draw(surf)


@start(SayText)
def _say_text_start():

    self: SayText = this()

    show()
    change_color(0, 0, 0)

    start = basics.timer_since_start()

    while basics.timer_since_start() - start < self.life and not self.follow.dead:
        move_to(self.follow.pos.x, self.follow.pos.y + ScreenToWorldFactorY(-self.follow._aabb_screen().h / 2 - 10))
        wait()
    
    delete()


def say(txt: str, time: float = None):
    """
    Display text above the current sprite
    """
    no_time = time is None
    time = time or float('inf')

    s = SayText(this(), time)
    s.text = txt

    if not no_time:
        wait(time)



    
_all_objects: list[GameObject] = []
_all_starts: list[object] = []