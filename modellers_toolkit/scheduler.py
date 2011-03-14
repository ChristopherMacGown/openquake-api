import eventlet
import threading
from eventlet import tpool

POOL = eventlet.GreenPool()

def schedule(task):
    eventlet.spawn_after(1, task)
