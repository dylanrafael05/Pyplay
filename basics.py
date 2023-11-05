import pygame
import time

_scr: pygame.Surface = None
_start_time: float = 0
_time: float = 0
_clock: pygame.time.Clock = None


def running() -> bool:
    return _scr is not None

def screen_surface() -> pygame.Surface:
    return _scr


def timer():
    """
    Get the current time since the timer started
    """
    return time.time() - _time

def timer_since_start():
    """
    Get the current time since the game started
    """
    return time.time() - _start_time

def restart_timer():
    """
    Reset the timer
    """
    _time = time.time()

def fps():
    """
    Get the current fps
    """
    return _clock.get_fps()