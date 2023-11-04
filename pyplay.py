import pygame
import threading
import time

import threads

from threads import *
from sprite import *
from events import *

SCREEN_DIMS = 1000, 666

def run():
    pygame.init()
    scr = pygame.display.set_mode(SCREEN_DIMS)

    timer = pygame.time.Clock()

    for spr in all_sprites:
        threads.spawner = spr
        for os in spr._on_start:
            os()
            
    threads.spawner = None

    for str in all_starts:
        str()

    while True:
        advance_frame()
        scr.fill('#FFFFFF')

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit(0)

        for spr in all_sprites:
            spr._draw(scr)

        pygame.display.update()

        timer.tick(60)