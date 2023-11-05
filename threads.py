import threading
import time
from typing import Any
from dataclasses import dataclass

_cur_spr_global = None

def maybe_this():
    cth = _cur_thread()
    if not cth:
        return _cur_spr_global
    sp = cth.spawner
    return sp

def this():
    thr = maybe_this()
    if thr is None:
        raise NoFoundSpriteError()
    return thr

def assign_this_unsafe(spr):
    global _cur_spr_global
    cth = _cur_thread()
    if not cth:
        _cur_spr_global = spr   
    else:
        cth.spawner = spr

spawner = None

class InvalidThreadCallError(Exception):
    pass

class NoFoundSpriteError(Exception):
    pass

class ThreadKilledError(Exception):
    pass

class WaitRequest:
    def __init__(self, amt: float = -1) -> None:
        super().__init__()
        self.start = time.time()
        self.amt = amt
    def check(self) -> bool:
        return (time.time() - self.start) >= self.amt


class PyplayThread(threading.Thread):
    def __init__(self, f, spawner):
        super().__init__(
            name = f'{f.__name__}+{time.time_ns()}',
            daemon = True
        )

        self._fn = f

        self.wait_for_main = threading.Event()
        self.wait_for_this = threading.Event()
        self.wait_req: WaitRequest = None
        self.spawner = spawner

        self.dead = False
        self.waited_on_by_main = False
        self.waiting_for_main = False

    def run(self):
        
        try:
            self._fn()
        except ThreadKilledError:
            pass
            
        self.kill()

    def mark_kill(self):

        self.dead = True

    def kill(self):

        self.mark_kill()

        if self.waited_on_by_main:
            self.wait_for_this.set()

        if self.spawner:
            with self.spawner._lock:
                self.spawner._threads.remove(self)
        
        del _running_threads[threading.current_thread().name]


_running_threads: dict[str, PyplayThread] = {}

def _cur_thread():
    if threading.current_thread().name not in _running_threads: return None
    return _running_threads[threading.current_thread().name]

def thread_kill_check():
    cth = _cur_thread()
    if cth is not None and cth.dead:
        raise ThreadKilledError()

def thread_operation(name):
    if threading.current_thread().name not in _running_threads:
        raise InvalidThreadCallError(f'Cannot call {name} outside of a script!')
    
    cth = _cur_thread()

    if cth.waited_on_by_main:
        cth.wait_for_this.set()

    thread_kill_check()

def wait(sec: float = -1):
    thread_operation('wait')
    
    cth = _cur_thread()

    cth.wait_req = WaitRequest(sec)

    cth.waiting_for_main = True
    cth.wait_for_main.wait()
    cth.wait_for_main.clear()
    
    thread_kill_check()

def script(f):

    def inner():
        
        # Create thread instance
        global spawner
        spwner = spawner
        
        if spwner is None:
            f()
            return

        thr = PyplayThread(f, spwner)

        spwner._threads.append(thr)
        _running_threads[thr.name] = thr
        
        spwner = None

        thr.start()

        return thr
    
    inner.__name__ = f.__name__
    inner.__doc__ = f.__doc__

    return inner