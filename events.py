from typing import Any
from sprite import Sprite
from threads import script

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