#!/usr/bin/env python

import os
import eventlet
import eventlet.debug

os.environ["EVENTLET_NOPATCH"] = 'True'
eventlet.monkey_patch()
#eventlet.debug.hub_prevent_multiple_readers(False)

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
