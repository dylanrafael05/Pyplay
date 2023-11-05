from typing import Any
from sprite import Sprite, all_sprites
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
    for spr in all_sprites:
        for e in spr._events(event):
            e(*args, **kwargs)



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