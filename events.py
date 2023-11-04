from typing import Any

class Event:
    def __init__(self) -> None:
        _event_map[self] = []

_event_map: dict[Event, list[Any]] = {}

def on(event: Event):
    def inner(f):
        _event_map[event].append(f)
        return f
    return inner

def broadcast(event: Event, *args, **kwargs):
    for e in _event_map[event]:
        e(*args, **kwargs)