from pyplay import *



cat = Sprite('katana1.png')
cat.x = 500
cat.y = 500



@start(cat)
@script
def cat_spawn():

    wait(10)
    delete(cat)


run()