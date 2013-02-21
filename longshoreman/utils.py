#!/usr/bin/env python


"""
Misc. utility functions
"""

import grp
import os
import pwd
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

def get_username():
    return pwd.getpwuid(os.getuid()).pw_name

def get_primary_group_name(username=None):
    if username is None:
        username = get_username()
    gid = pwd.getpwnam(username).pw_gid
    return grp.getgrgid(gid).gr_name

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

