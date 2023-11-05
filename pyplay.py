import pygame
import threading
import time
import random

import threads

from threads import *
from sprite import *
from events import *
from sound import *

SCREEN_DIMS = 1000, 666

_scr: pygame.Surface
_time: float

def screen_surface():
    return _scr

def stop_all():
    """
    Quit this game    
    """
    pygame.quit()
    exit()

def pick_random(start: float, end: float):
    """
    Get a random number between the two provided
    """
    return random.random() * (end - start) + start

def timer():
    """
    Get the current time since the timer started
    """
    return time.time() - _time

def restart_timer():
    """
    Reset the timer
    """
    global _time
    _time = time.time()

def run():
    global _scr, _time

    pygame.init()
    _scr = pygame.display.set_mode(SCREEN_DIMS)

    _time = time.time()

    timer = pygame.time.Clock()

    for spr in all_sprites:
        for os in spr._on_start:
            threads.spawner = spr
            os()
    
    threads.spawner = None

    for str in all_starts:
        str()

    while True:
        _scr.fill('#FFFFFF')

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit(0)
                case pygame.KEYDOWN:
                    broadcast_key_press(event.key)
                case pygame.MOUSEBUTTONDOWN:
                    broadcast_mouse_click()

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
            spr._draw(_scr)

        pygame.display.update()

        timer.tick(60)

def mouse_x():
    return pygame.mouse.get_pos()[0]
def mouse_y():
    return pygame.mouse.get_pos()[1]

get_mouse_pos = pygame.mouse.get_pos