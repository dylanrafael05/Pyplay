import pygame
import threads

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

all_sprites: list[Sprite] = []
all_starts: list[object] = []