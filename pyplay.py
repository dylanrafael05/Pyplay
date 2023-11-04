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
        for os in spr._on_start:
            threads.spawner = spr
            os()
    
    threads.spawner = None

    for str in all_starts:
        str()

    while True:
        scr.fill('#FFFFFF')

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit(0)

        for spr in all_sprites:
            for thread in spr._threads:
                if thread.waiting_for_main and thread.wait_req.check():
                    with thread.wait_for_main:
                        thread.wait_for_main.notify()
                    thread.waited_on_by_main = True
                    with thread.wait_for_this:
                        thread.wait_for_this.wait()
                        thread.waited_on_by_main = False


        for spr in all_sprites:
            spr._draw(scr)

        pygame.display.update()

        timer.tick(60)