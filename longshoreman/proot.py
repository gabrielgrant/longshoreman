#!/usr/bin/env python

"""
proot.py

Interface to create and manage PRoots
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
    
    # mounting happens at command execution time, so we're done

def get_proot_command(
    proot_filepath='./PRoot-2.3.1/src/proot',
    fakeroot='/tmp/fakeroot',
    command=None
):
    cmds = [proot_filepath]
    mount_dir_cmds = []
    for target in BIND_DIRS:
        mount_dir_cmds.append('-b')
        #link_name = in_fakeroot(target)
        #mount_dir_cmds.append('%s:%s' % (target, link_name))
        mount_dir_cmds.append(target)

    cmds.extend(mount_dir_cmds)
    cmds.extend(['-r', fakeroot])
    if command:
        cmds.append(command)
    return cmds


USAGE = """proot.py CONTAINER_DIR

Creates a container template in the provided directory

CONTAINER_DIR  a non-existent path
"""

def main(args):
    if len(args) != 1:
        print 'Exactly one argument required.\n'
        print USAGE
        return
    if args[0] in ('-h', '--help'):
        print USAGE
        return
    fakeroot = args[0]
    if os.path.exists(fakeroot):
        print 'The directory location is not empty:', fakeroot, '\n'
        print USAGE
        return
    create_proot(fakeroot)
    print ' '.join(get_proot_command(fakeroot))

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
