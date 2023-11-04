from pyplay import *


cat = Sprite('katana1.png')
cat.x = 500
cat.y = 500


cat_dead = Event()


@start(cat)
@script
def cat_spawn():

    wait(1)
    change_color(255, 0, 0)

    broadcast(cat_dead)


@start(cat)
@script
def cat_spawn2():

    while True:
        wait()
        print(f"{time.time()}")


@on(cat_dead)
def cat_is_dead():
    print("noooooo!")


run()