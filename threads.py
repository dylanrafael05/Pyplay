import threading
import typing
from dataclasses import dataclass

@dataclass
class Thread:
    thr: threading.Thread
    cond: threading.Condition

    def start(self):
        self.thr.start()


running_threads: dict[str, Thread] = {}

def coroutine(f):

    def inner():
        thr = Thread(
            threading.Thread(
                target=f,
                daemon=True
            ),
            threading.Condition()
        )

        running_threads[f.__name__] = thr
        thr.start()

        return thr
    
    inner.__name__ = f.__name__
    inner.__doc__ = f.__doc__

    return inner