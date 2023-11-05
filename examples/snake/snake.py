from pyplay import *

snake = Sprite("snake.png")
apple = Sprite("apple.png")

lose = Event()
eat_apple = Event()

nom = Sound("nom.ogg")

score = 0

@start(snake)
def snake_start():
    move_to(0, 0)
    change_size(100)
    this().speed = 1
    while True:
        move_forward(this().speed)
        if is_touching_edge():
            broadcast(lose)
        wait()

@start(apple)
def apple_start():
    go_to_random_position()
    while True:
        if (is_touching(snake)):
            broadcast(eat_apple)
            go_to_random_position()
        wait()

@on(key_a_press, snake)
def turn_left():
    rotate(-90)
@on(key_d_press, snake)
def turn_left():
    rotate(90)

@on(lose)
def reset_game():
    print("you lose! Score: " + str(score))
    move_to(0, 0)
    rotate_to(0)
    snake.speed = 1
    say("Score: " + str(score))

@on(eat_apple, snake)
def ate_apple():
    global score
    print("yum yum")
    play_sound(nom)
    snake.speed += 1
    score += 1
    say("Score: " + str(score))

run("snake")