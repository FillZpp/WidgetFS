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
os.chdir(wfs_home_path)

# check version of python
if sys.version_info < (3,):
    py_version = 2
else:
    py_version = 3

master_host = 'localhost'
client_port = 12180
tcp_client = socket(AF_INET, SOCK_STREAM)


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
    with open('etc/wfs_client.cfg') as ff:
        cfg_list = ff.readlines()
    for i in cfg_list:
        i = i.strip()
        if not i or i.startswith('#'):
            continue
        mkey, mvalue = [s.strip() for s in i.split('=')]
        if mkey == 'master_host':
            master_host = mvalue
        elif mkey == 'client_port':
            client_port = int(mvalue)
    master_host = gethostbyname(master_host)


def get_connection():
    """Get connection with master server"""
    try:
        tcp_client.connect((master_host, client_port))
        if py_version == 3:
            data = bytes('0000', 'utf-8')
        else:
            data = '0000'
        tcp_client.send(data)
        recv = tcp_client.recv(4)
        print(recv)
    except error as e:
        sys.stderr.write('Error:\n')
    finally:
        tcp_client.close()


def do_mkdir(pars):
    """Send mkdir command"""
    get_connection()


def do_ls(pars):
    """Send ls command"""
    get_connection()


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
    

