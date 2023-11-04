import threading
import time
from typing import Any
from dataclasses import dataclass

def get_current_sprite():
    sp = _cur_thread().spawner
    if sp is None:
        raise NoFoundSpriteError()
    return sp

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

@dataclass
class Thread:
    thr: threading.Thread
    wait_for_main: threading.Condition
    wait_for_this: threading.Condition
    wait_req: WaitRequest
    spawner: Any
    
    dead: bool = False
    waited_on_by_main: bool = False
    waiting_for_main: bool = False

    def start(self):
        self.thr.start()

    def kill(self):
        self.dead = True
        
        if self.waited_on_by_main:
            with self.wait_for_this:
                self.wait_for_this.notify()

        if self.spawner:
            self.spawner._threads.remove(self)
        
        del _running_threads[threading.current_thread().name]

_running_threads: dict[str, Thread] = {}

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
        _cur_thread().wait_for_this.notify()

    thread_kill_check()

def wait(sec: float = -1):
    thread_operation('wait')
    
    cth = _cur_thread()

    cth.wait_req = WaitRequest(sec)

    with cth.wait_for_main:
        cth.waiting_for_main = True
        cth.wait_for_main.wait()
    
    thread_kill_check()

def script(f):

    def inner(*args, **kwargs):
        
        # Create thread instance
        global spawner

        if not spawner:
            f(*args, **kwargs)
            return
    
        # Handles threadkillederror without crash,
        # then kills the thread.
        def f_wrap():

            try:
                f(*args, **kwargs)
            except ThreadKilledError:
                pass
                
            thr.kill()

        thr = Thread(
            threading.Thread(
                name=f'{f.__name__}.{time.time_ns()}',
                target=f_wrap,
                daemon=True
            ),
            threading.Condition(),
            threading.Condition(),
            None,
            spawner
        )

        spawner._threads.append(thr)
        _running_threads[thr.thr.name] = thr
        
        spawner = None

        thr.start()

        return thr
    
    inner.__name__ = f.__name__
    inner.__doc__ = f.__doc__

    return inner