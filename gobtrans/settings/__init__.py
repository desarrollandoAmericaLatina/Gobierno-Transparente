# -*- coding: utf-8 -*-
"""
There are 3 types of settings.
1) System. Stays the same for every project.
2) Local. Specific to each instance of the project. Not versioned.
3) Debug. Applies for debugging. Forbidden for production use.
"""
import logging

from .system import *
try:
    from .local import *
except ImportError, e:
    logging.warning("Couldn't find local settings: %s" % str(e))
if DEBUG:
    try:
        from .debug import *
    except ImportError, e:
        pass
