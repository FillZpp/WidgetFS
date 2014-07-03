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
from binascii import crc32
from socket import *


master_host = 'localhost'
master_port = 12180
block_size = 64*1024


def turn_bytes(s):
    if sys.version_info >= (3,):
        return bytes(s, 'utf-8')
    return s


def calculate_crc(content):
    c = crc32(turn_bytes(content))
    c = crc32(turn_bytes(content), c) & 0xffffffff
    return bin(c).lstrip('0b')


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


def get_connection():
    """Get connection with master server"""
    tcp_client = socket(AF_INET, SOCK_STREAM)
    try:
        tcp_client.connect((master_host, master_port))
        tcp_client.send(turn_bytes('0000'))
        recv = tcp_client.recv(4).decode('utf-8')
    except error as e:
        sys.stderr.write('Error:\n' + e.strerror)
        tcp_client.close()
    return tcp_client


def do_mkdir(pars):
    """Send mkdir command"""
    if len(pars) == 0:
        print_help()
        return
        
    for par in pars:
        tcp_client = get_connection()
        try:
            tcp_client.send(turn_bytes('1001'))
            tcp_client.send(turn_bytes(par))
            recv = tcp_client.recv(1024).decode('utf-8')
            print(recv)
        except error as e:
            sys.stderr.write('Error:\n' + e.strerror + '\n')
        tcp_client.close()


def do_rmdir(pars):
    """Send rmdir command"""
    if len(pars) == 0:
        print_help()
        return

    for par in pars:
        tcp_client = get_connection()
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
    tcp_client = get_connection()

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


def do_mknod(pars):
    """Send mknod command"""
    if len(pars) == 0:
        print_help()
        return

    for par in pars:
        tcp_client = get_connection()
        try:
            tcp_client.send(turn_bytes('0001'))
            tcp_client.send(turn_bytes(par))
            recv = tcp_client.recv(1024).decode('utf-8')
            print(recv)
        except error as e:
            sys.stderr.write('Error:\n' + e.strerror + '\n')
        finally:
            tcp_client.close()


def do_put(pars):
    """Put a file into Widget file system"""
    if len(pars) != 2:
        print_help()
        return

    if not os.path.isfile(pars[0]):
        print('%s is not a file' % pars[0])
        return

    # mknod first
    do_mknod([pars[1]])

    with open(pars[0], 'r') as ff:
        lines = ff.readlines()
    content = ''.join(lines)

    num = len(content) // block_size
    if (len(content) % block_size) != 0:
        num += 1

    tcp_client = get_connection()
    try:
        tcp_client.send(turn_bytes('0011'))
        tcp_client.send(turn_bytes(pars[1]))
        tcp_client.send(turn_bytes(str(num)))
        recv = tcp_client.recv(4).decode('utf-8')
        if recv != '1111':
            print('Put error')
            return
    except error as e:
        sys.stderr.write('Error:\n' + e.strerror + '\n')
    

    for i in range(0, num):
        if i != num-1:
            seg = content[i*block_size:(i+1)*block_size]
        else:
            seg = content[i*block_size:]
        crc = calculate_crc(seg)
        while True:
            tcp_client.send(turn_bytes(crc))
            tcp_client.send(turn_bytes(seg))
            recv = tcp_client.recv(4).decode('utf-8')
            if recv == '1111':
                break
        
    tcp_client.close()

def main():
    if len(sys.argv) == 1:
        print_help()

    elif sys.argv[1] == 'ls':
        do_ls(sys.argv[2:])
        
    elif sys.argv[1] == 'mkdir':
        do_mkdir(sys.argv[2:])
        
    elif sys.argv[1] == 'rmdir':
        do_rmdir(sys.argv[2:])
        
    elif sys.argv[1] == 'mknod':
        do_mknod(sys.argv[2:])

    elif sys.argv[1] == 'cat':
        do_cat(sys.argv[2:])

    elif sys.argv[1] == 'put':
        do_put(sys.argv[2:])

    elif sys.argv[1] == 'get':
        do_get(sys.argv[2:])

    elif sys.argv[1] == 'rm':
        do_rm(sys.argv[2:])
    
    else:
        print_help()


if __name__ == '__main__':
    main()
    

