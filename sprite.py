import random
import pygame
from threads import get_current_sprite, wait_frame

class Sprite:

    def __init__(self, *all_costumes: str) -> None:
        self.x = 0
        self.y = 0
        self.angle = 0
        self.size = 100

        self.costume = 0

        self.shown = True


        self._all_costumes = Sprite._load_all_images(all_costumes)

        self._on_start = []

        all_sprites.append(self)

    @staticmethod
    def _load_all_images(filenames: list[str]) -> list[pygame.surface.Surface]:

        out = []

        for filename in filenames:
            out.append(pygame.image.load(filename))
        
        return out
    
    @property
    def image(self) -> pygame.surface.Surface:
        return self._all_costumes[self.costume] 

    def _draw(self, surf: pygame.surface.Surface):

        rot_img: pygame.surface.Surface = \
            pygame.transform.rotozoom(self.image, self.angle, self.size / 100)

        surf.blit(
            rot_img,
            pygame.Vector2(
                self.x - rot_img.get_width() / 2, 
                self.y - rot_img.get_height() / 2
            )
        )


def start(spr: Sprite = None):
    """
    Defines a script to be run when a sprite is spawned.
    """

    if spr is not None:

        def inner(f):
            spr._on_start.append(f)
            return f
        return inner

    else:

        def inner(f):
            all_starts.append(f)
            return f
        return inner

def delete(spr: Sprite):
    """
    Deletes a sprite.
    """
    all_sprites.remove(spr)
    threads.kill_spawner(spr)

def change_size(factor: int):
    ''' changes the size by a specific number'''
    threads.get_current_sprite().size = (factor * 100)

def percent_size(percent : int):
    threads.get_current_sprite().size = percent

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
        wait_frame()
        spr.x = xstart + xdiff * (i / frames)
        spr.y = ystart + ydiff * (i / frames)
            
    
all_sprites: list[Sprite] = []
all_starts: list[object] = []