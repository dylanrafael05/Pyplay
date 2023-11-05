from pyplay import *

apple = Sprite("katana1.png")
apple.x = 500
apple.y = 500

apple_eaten = Event()
@clone_start(apple)
def apple_clone():

    print("START ", time.time())
    i = 0

    while i < 5:

        wait(.1)

        go_to_random_position()
        set_size(100)
        change_color(0, 255, 0)

        change_color(0, 0, 255)
        change_size(10)

        move()
        clone()

        i += 1

@script
def move():
    print("moved")
    glide_to_position(300,400,5)


@start(apple)
def apple_spawn():
    print('STARTTTT')
    clone()


run()