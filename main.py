from pyplay import *


cat = Sprite('katana1.png')
cat.x = 500
cat.y = 500


cat_dead = Event()


@clone_start(cat)
@script
def cat_clone():

    get_current_sprite().x = random.randrange(0, 1000)
    get_current_sprite().y = random.randrange(0, 1000)

    cat_spawn()


@start(cat)
@script
def cat_spawn():

    wait(1)
    
    clone()
    change_color(255, 0, 0)

    broadcast(cat_dead)


@start(cat)
@script
def cat_spawn2():

    while True:
        wait()
        print(f"{time.time()}")


@on(cat_dead, cat)
def cat_is_dead():
    print("noooooo!")


run()