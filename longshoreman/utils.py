#!/usr/bin/env python


"""
Misc. utility functions
"""

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
