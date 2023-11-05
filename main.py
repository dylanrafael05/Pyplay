from pyplay import *


cat = Sprite('python py.png')
cat.x = 500
cat.y = 333

cat_x = Sprite('python py.png')
cat_y = Sprite('python py.png')


cat_dead = Event()

@start(cat)
def cat_start():
    while True:
        move_to(mouse_x(), mouse_y())
        wait()

@start(cat_x)
def start_x():
    while True:
        move_to(mouse_x(), 100)
        wait()

@start(cat_y)
def start_y():
    while True:
        move_to(100, mouse_y())
        wait()

run()