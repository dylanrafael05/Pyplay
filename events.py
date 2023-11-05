from typing import Any
from sprite import Sprite, _all_objects
import threads
from threads import script
import pygame

class Event:
    def __init__(self) -> None:
        _global_event_map[self] = []

_global_event_map: dict[Event, list[Any]] = {}

def on(event: Event, spr: Sprite = None):

    if spr is None:
        def inner(f):
            f = script(f)
            _global_event_map[event].append(f)
            return f
        return inner
    else:
        def inner(f):
            f = script(f)
            spr._add_event(event, f)
            return f
        return inner


def broadcast(event: Event, *args, **kwargs):
    for e in _global_event_map[event]:
        e(*args, **kwargs)
    for spr in _all_objects:
        for e in spr._events(event):
            threads.spawner = spr
            e(*args, **kwargs)
        threads.spawner = None



# Key press
key_press_events = dict[int, Event]()
def key_press(key: int): # Event
    if (key not in key_press_events):
        key_press_events[key] = Event()
    return key_press_events[key]

def broadcast_key_press(key: int):
    if (key not in key_press_events):
        return
    broadcast(key_press_events[key])

def get_key_down(key: int):
    return pygame.key.get_pressed()[key]

mouse_click_event = Event()
def mouse_click():
    return mouse_click_event
def broadcast_mouse_click():
    broadcast(mouse_click_event)


key_a_press = key_press(pygame.K_a)
key_b_press = key_press(pygame.K_b)
key_c_press = key_press(pygame.K_c)
key_d_press = key_press(pygame.K_d)
key_e_press = key_press(pygame.K_e)
key_f_press = key_press(pygame.K_f)
key_g_press = key_press(pygame.K_g)
key_h_press = key_press(pygame.K_h)
key_i_press = key_press(pygame.K_i)
key_j_press = key_press(pygame.K_j)
key_k_press = key_press(pygame.K_k)
key_l_press = key_press(pygame.K_l)
key_m_press = key_press(pygame.K_m)
key_n_press = key_press(pygame.K_n)
key_o_press = key_press(pygame.K_o)
key_p_press = key_press(pygame.K_p)
key_q_press = key_press(pygame.K_q)
key_r_press = key_press(pygame.K_r)
key_s_press = key_press(pygame.K_s)
key_t_press = key_press(pygame.K_t)
key_u_press = key_press(pygame.K_u)
key_v_press = key_press(pygame.K_v)
key_w_press = key_press(pygame.K_w)
key_x_press = key_press(pygame.K_x)
key_y_press = key_press(pygame.K_y)
key_z_press = key_press(pygame.K_z)
key_0_press = key_press(pygame.K_0)
key_1_press = key_press(pygame.K_1)
key_2_press = key_press(pygame.K_2)
key_3_press = key_press(pygame.K_3)
key_4_press = key_press(pygame.K_4)
key_5_press = key_press(pygame.K_5)
key_6_press = key_press(pygame.K_6)
key_7_press = key_press(pygame.K_7)
key_8_press = key_press(pygame.K_8)
key_9_press = key_press(pygame.K_9)
key_left_press = key_press(pygame.K_LEFT)
key_right_press = key_press(pygame.K_RIGHT)
key_up_press = key_press(pygame.K_UP)
key_down_press = key_press(pygame.K_DOWN)
key_space_press = key_press(pygame.K_SPACE)