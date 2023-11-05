from pyplay import *

apple = Sprite("katana1.png")
apple._x_scr = 500
apple._y_scr = 500

apple_eaten = Event()


sus = Text()

@start(sus)
def sus_start():
    move_to(0, 0)
    change_color(0, 0, 0)

    while True:
        set_text(str(fps()))
        wait()

@clone_start(apple)
def apple_clone():

    i = 0

    while i < 2:

        go_to_random_position()
        set_size(100)
        change_color(0, 255, 0)

        wait()

        say(f'Hello! {i}')

        change_color(0, 0, 255)
        change_size(10)

        move()
        clone()

        i += 1

    delete()

@on(key_0_press)
def move():
    glide_to_position(0,0,1)


@start(apple)
def apple_spawn():
    clone()


run("Example")