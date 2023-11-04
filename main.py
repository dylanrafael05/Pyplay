import pygame
import threading
import time

import threads

SCREEN_DIMS = 1000, 666

def wait(sec):
    time.sleep(sec)

@threads.coroutine 
def wow():
    wait(1)
    print('Hello world!')

def main():
    pygame.init()
    scr = pygame.display.set_mode(SCREEN_DIMS)

    timer = pygame.time.Clock()

    while True:
        scr.fill('#000000')

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    exit(0)
                case pygame.KEYDOWN:
                    wow()

        timer.tick(60)

if __name__ == '__main__':
    main()