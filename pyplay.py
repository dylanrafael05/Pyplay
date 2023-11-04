import pygame
import threading
from threads import script
import time
from sprite import *

import threads

SCREEN_DIMS = 1000, 666

def wait(sec):
    time.sleep(sec)

def run():
    pygame.init()
    scr = pygame.display.set_mode(SCREEN_DIMS)

    timer = pygame.time.Clock()

    for spr in all_sprites:
        spr._on_start()

    for str in all_starts:
        str()

    while True:
        scr.fill('#000000')

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit(0)

        for spr in all_sprites:
            spr._draw(scr)

        pygame.display.update()

        timer.tick(60)