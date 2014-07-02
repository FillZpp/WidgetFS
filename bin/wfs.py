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
from widgetfs.conf.codef import turn_bytes


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
        tcp_client.send(turn_bytes('0000'))
        recv = tcp_client.recv(4).decode('utf-8')
    except error as e:
        sys.stderr.write('Error:\n')
        tcp_client.close()


def do_mkdir(pars):
    """Send mkdir command"""
    if len(pars) == 0:
        print_help()
        return
        
    for par in pars:
        get_connection()
        try:
            tcp_client.send(turn_bytes('1001'))
            tcp_client.send(turn_bytes(par))
            recv = tcp_client.recv(1024).decode('utf-8')
            print(recv)
        except error as e:
            sys.stderr.write('Error:\n' + e.strerror + '\n')
        finally:
            tcp_client.close()


def do_rmdir(pars):
    """Send rmdir command"""
    if len(pars) == 0:
        print_help()
        return

    for par in pars:
        get_connection()
        try:
            tcp_client.send(turn_bytes('1100'))
            tcp_client.send(turn_bytes(par))
            recv = tcp_client.recv(1024).decode('utf-8')
            print(recv)
        except error as e:
            sys.stderr.write('Error:\n' + e.strerror + '\n')
        finally:
            tcp_client.close()


def do_ls(pars):
    """Send ls command"""
    get_connection()

    try:
        tcp_client.send(turn_bytes('1000'))

        if len(pars) == 0:
            tcp_client.send(turn_bytes('/'))
        else:
            tcp_client.send(turn_bytes(pars[0]))
        
        recv = tcp_client.recv(1024).decode('utf-8')
        print(recv)
    except error as e:
        sys.stderr.write('Error:\n' + e.strerror + '\n')
    finally:
        tcp_client.close()


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
    

