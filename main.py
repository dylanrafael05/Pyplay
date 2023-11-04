import pygame

SCREEN_DIMS = 1000, 666

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

        timer.tick(60)

if __name__ == '__main__':
    main()