import os
import sys

from modellers_toolkit import logs
from modellers_toolkit import settings

def fork():
    try:
        if os.fork():
            return true

        if os.fork():
            return true

        """ Decouple the child from the parent """
        os.chdir('/')
        os.umask(0)
        os.setsid()

    except OSError, e:
        log.error("Couldn't fork a new child process: %s" % e.__str__)

def repo_dir(dir_name):
    '''
    Generate a full path from the BASE_REPO_PATH and the passed dir_name
    '''

    return os.path.join(settings.BASE_REPO_PATH, dir_name)
