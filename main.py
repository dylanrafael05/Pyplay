from pyplay import *


cat = Sprite('python py.png')
cat.x = 500
cat.y = 500


meow = Sound('meow.ogg')


cat_dead = Event()

@script
def x():
    wait(1)


@clone_start(cat)
def cat_clone():

    print("START ", time.time())

    x()

    with cat:
        move(10, 10)

    play_sound(meow)

    go_to_random_position()
    set_size(100)
    change_color(255, 255, 255)

    wait(2.5)

    clone()

    change_color(255, 0, 0)
    change_size(10)


@start(cat)
def cat_spawn():
    print('STARTTTT')
    clone()


# @start(cat)
# def cat_spawn2():

#     while True:
#         wait()


@on(cat_dead, cat)
@on(key_press(pygame.K_0), cat)
def cat_is_dead():
    print("noooooo!")


run()