#! /usr/bin/env python


"""
Copyright (C) 2014 FillZpp

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


import os
import sys
from socket import *
wfs_home_path = os.environ.get('WFS_HOME')
if not wfs_home_path:
    sys.stderr.write('Error:\n  ' +
                     'You should define environment variable WFS_HOME first.\n')
    sys.exit(-1)
sys.path.append(wfs_home_path)


def print_help():
    """Print wfs help"""
    print('Widget file system client\n' +
          'Usage: wfs [option] ... [args]\n' +
          '  mkdir       [directory]\n' +
          '  rmdir       [directory]\n' +
          '  mknod       [file]\n' +
          '  cat         [file]\n' +
          '  ls          [file | directory]\n' +
          '  cp          [file | directory]\n' +
          '  mv          [file | directory]\n' +
          '  rm          [file | directory]')


def read_cfg():
    """Read config file"""
    #with open('etc/')
    pass


def do_mkdir(pars):
    pass


def do_ls():
    pass


def main():
    if len(sys.argv) == 1:
        print_help()
        
    elif sys.argv[1] == 'mkdir':
        do_mkdir(sys.argv[2:])
        
    elif sys.argv[1] == 'rmdir':
        do_rmdir(sys.argv[2:])
        
    elif sys.argv[1] == 'mknod':
        do_mknod(sys.argv[2:])

    elif sys.argv[1] == 'cat':
        do_cat(sys.argv[2:])

    elif sys.argv[1] == 'ls':
        do_ls(sys.argv[2:])

    elif sys.argv[1] == 'cp':
        do_cp(sys.argv[2:])

    elif sys.argv[1] == 'mv':
        do_mv(sys.argv[2:])

    elif sys.argv[1] == 'rm':
        do_rm(sys.argv[2:])
    
    else:
        print_help()


if __name__ == '__main__':
    main()
    

