#!/usr/bin/env python

"""
create_proot.py

replace this with a description of the code and write the code below this text.
"""

import os

BIND_DIRS = [
    '/bin',
    '/sbin',
    '/dev',
    '/etc',
    '/lib',
    '/usr',
    '/proc',
]

LINK_DIRS = [
    ('/lib', 'lib64'),
]

MK_DIRS = [
    '/home',
    '/tmp',
    '/var',
    '/opt', # for system installs
]



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

def create_proot(fakeroot='/tmp/fakeroot'):
    def in_fakeroot(path):
        fakeroot_path = '/'.join([fakeroot, path])
        return os.path.normpath(fakeroot_path)

    print 'fakeroot', fakeroot

    # make directories
    for d in BIND_DIRS + MK_DIRS:
        newdir = in_fakeroot(d)
        print 'making', newdir
        mkdir_p(newdir)

    # make links
    for target, link_name in LINK_DIRS:
        fakeroot_link_name = in_fakeroot(link_name)
        print 'linking', fakeroot_link_name, 'to', target
        os.symlink(target, fakeroot_link_name)

    mount_dir_cmds = []
    for target in BIND_DIRS:
        mount_dir_cmds.append('-b')
        #link_name = in_fakeroot(target)
        #mount_dir_cmds.append('%s:%s' % (target, link_name))
        mount_dir_cmds.append(target)

    print './PRoot-2.3.1/src/proot', ' '.join(mount_dir_cmds), '-r', fakeroot

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
