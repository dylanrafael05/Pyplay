import threading
import time
from typing import Any
from dataclasses import dataclass

def get_current_sprite():
    return _cur_thread().spawner

def advance_frame():
    for thr in _running_threads.values():
        thr.frame = True

spawner = False

class ThreadKilledError(Exception):
    pass

@dataclass
class Thread:
    thr: threading.Thread
    frame: bool
    dead: bool
    spawner: Any

    def start(self):
        self.thr.start()

    def kill(self):
        self.dead = True

_running_threads: dict[str, Thread] = {}
_threads_by_spawner: dict[Any, list[Thread]] = {}

def kill_spawner(spawner):
    if spawner in _threads_by_spawner:
        _threads_by_spawner[spawner].kill()

def _cur_thread():
    return _running_threads[threading.current_thread().name]

def thread_kill_check():
    if _cur_thread().dead:
        raise ThreadKilledError()

def thread_operation(name):
    if threading.current_thread().name not in _running_threads:
        print(f'Cannot call {name} outside of a script!')
        exit(-1)
    
    thread_kill_check()

def wait(sec: float = -1):
    thread_operation('wait')
    
    if sec == -1:
        wait_frame()
    else:
        time.sleep(sec)
        thread_kill_check()

def wait_frame():
    thread_operation('wait_frame')

    while not _cur_thread().frame:
        time.sleep(0.001)
        
    _cur_thread().frame = False

def kill_spawner(spawner):
    if spawner in _threads_by_spawner:
        for thr in _threads_by_spawner[spawner]:
            thr.kill()

def script(f):

    def inner():

        def f_wrap(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except ThreadKilledError:
                pass
        

        thr = Thread(
            threading.Thread(
                name=f.__name__,
                target=f_wrap,
                daemon=True
            ),
            False,
            False,
            spawner
        )

        _running_threads[f.__name__] = thr
        if spawner: 
            if spawner in _threads_by_spawner:
                _threads_by_spawner[spawner].append(thr)
            else:
                _threads_by_spawner[spawner] = []

        thr.start()

        return thr
    
    inner.__name__ = f.__name__
    inner.__doc__ = f.__doc__

    return inner

def get_current_sprite():
    pass