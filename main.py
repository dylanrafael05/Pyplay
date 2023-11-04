from pyplay import *


cat = Sprite('katana1.png')
cat.x = 500
cat.y = 500


cat_dead = Event()


@clone_start(cat)
def cat_clone():

    print("START ", time.time())

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
def cat_is_dead():
    print("noooooo!")


run()