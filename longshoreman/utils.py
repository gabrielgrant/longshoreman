#!/usr/bin/env python


"""
Misc. utility functions
"""

import os
import socket

def get_free_port(exclude=None):
    """ Get an OS-assigned free port """
    if exclude is None:
      exclude = []
    while True:
      s = socket.socket()
      s.bind(('',0))
      address, port = s.getsockname()
      if port not in exclude:
          break
    return port

def mkdir_p(newdir):
    """ from http://code.activestate.com/recipes/82465-a-friendly-mkdir/
        works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir_p(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)

