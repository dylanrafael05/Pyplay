# Pyplay
PyPlay is a game engine that is designed to work like Scratch so that kids can start to code games as they get introduced to coding.
For full documentation, go to this repo's wiki!

## How to Use
To use PyPlay, copy its source files into your project directory and use the following template to get your game started!:
```py
# add pyplay's libraries
from pyplay import *

# add a sprite!
my_sprite = Sprite("image.png")

# write a start function!
@start(my_sprite)
def on_start():
    pass

# run your app!
run("My PyPlay Game")
```

See [the snake example](snake.py) for a more fleshed-out example!
