#!/usr/bin/env python
import os
import site
import sys

from os.path import abspath, dirname, join

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)
prev_sys_path = list(sys.path)

site.addsitedir(path('apps'))
site.addsitedir(path('lib'))
site.addsitedir(path('vendor'))

# Move the new items to the front of sys.path. (via virtualenv)
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

try:
    import pinax
except ImportError:
    sys.stderr.write("Error: Can't import Pinax. Make sure you are in a virtual environment that has\nPinax installed or create one with pinax-boot.py.\n")
    sys.exit(1)

from django.conf import settings
from django.core.management import setup_environ, execute_manager, execute_from_command_line

try:
    import settings_local as settings
except ImportError:
    try:
        import settings
    except ImportError:
        import sys
        sys.stderr.write(
            "Error: Tried importing 'settings_local.py' and 'settings.py' "
            "but neither could be found (or they're throwing an ImportError)."
            " Please come back and try again later.")
        raise

# setup the environment before we start accessing things in the settings.
setup_environ(settings)

if __name__ == "__main__":
    execute_manager(settings)
