import pygame
import threading
import time
import random

import threads
import basics
import sprite

from basics import *
from threads import *
from sprite import *
from events import *
from sound import *

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

def run(title: str = None):

    title = title or 'PyPlay Project'

    pygame.init()
    basics._scr = pygame.display.set_mode(SCREEN_DIMS)

    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.image.load('python py.png'))

    basics._start_time = time.time()
    basics._time = basics._start_time

    basics._clock = pygame.time.Clock()

    for spr in sprite._all_objects:
        spr._begin()

    for str in sprite._all_starts:
        str()

    while True:
        basics._scr.fill('#D0D0D0')

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit(0)
                case pygame.KEYDOWN:
                    broadcast_key_press(event.key)
                case pygame.MOUSEBUTTONDOWN:
                    broadcast_mouse_click()

        for spr in sprite._all_objects:
            for thread in spr._threads:
                if thread.waiting_for_main and thread.wait_req.check():

                    thread.wait_for_main.set()
                    thread.waiting_for_main = False

                    thread.waited_on_by_main = True
                    if not thread.wait_for_this.wait(1):
                        print('lockup.')
                    thread.wait_for_this.clear()


        for spr in sprite._all_objects:
            spr._draw(basics._scr)

        pygame.display.update()

        basics._clock.tick(60)

def mouse_x():
    return pygame.mouse.get_pos()[0]
def mouse_y():
    return pygame.mouse.get_pos()[1]

get_mouse_pos = pygame.mouse.get_pos