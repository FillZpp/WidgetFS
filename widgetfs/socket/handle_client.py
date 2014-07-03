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
from widgetfs.conf.config import common_cfg
from widgetfs.conf.codef import *
from widgetfs.core.meta import WfsMeta
from widgetfs.core.log import write_master_log
from widgetfs.core.chunk_ctrl import *


def handle_client_connection (client, addr):
    """Deal with client commands"""
    while True:
        ctrl_data = client.recv(4).decode('utf-8')
        if ctrl_data == '1000':
            do_ls(client, addr)
        elif ctrl_data == '1001':
            do_mkdir(client, addr)
        elif ctrl_data == '1100':
            do_rmdir(client, addr)

        elif ctrl_data == '0001':
            do_mknod(client, addr)
        elif ctrl_data == '0010':
            do_read(client, addr)
        elif ctrl_data == '0011':
            do_write(client, addr)
        elif ctrl_data == '0100':
            do_rm(client, addr)

        else:
            break
            
    write_master_log('Disconnect with client %s.' % str(addr))


def split_path (tar_path):
    """Part the path into list"""
    path_list = []
    tar_dir = tar_path
    while True:
        tar_dir, cdir = os.path.split(tar_dir)
        if cdir == '':
            path_list.insert(0, tar_dir)
            break
        path_list.insert(0, cdir)
    return path_list


def check_path (path_list):
    """Check if path is correct"""
    if path_list[0] != '/':
        return None, None
    elif len(path_list) == 1:
        return 'dir', WfsMeta.root_dir
        
    ndir = WfsMeta.root_dir
    n = 1
    while True:
        t = False
        ndir.rwlock.read_lock()
        for idir in ndir.cdirs:
            if path_list[n] == idir.dname:
                t = True
                ndir.rwlock.read_unlock()
                ndir = idir
                break
        if t:
            if n == len(path_list)-1:
                return 'dir', ndir
        else:
            ndir.rwlock.read_unlock()
            if n == len(path_list)-1:
                ndir.rwlock.read_lock()
                for ifile in ndir.files:
                    if path_list[n] == ifile.fname:
                        ndir.rwlock.read_unlock()
                        return 'file', ifile
            ndir.rwlock.read_unlock()
            return n, ndir
        n += 1


def do_ls (client, addr):
    """Command: ls"""
    tar_path = client.recv(1024).decode('utf-8')
    path_list = split_path(tar_path.strip())
    t, con = check_path(path_list)

    if t == 'file':
        write_master_log('client %s: ls %s. Done.' %
                         (addr, tar_path))
        client.send(turn_bytes('File: %s\nSize: %s' %
                    (con.fname, con.size)))
    elif t == 'dir':
        write_master_log('client %s: ls %s. Done.' %
                         (addr, tar_path))
        client.send(turn_bytes('ls: %s\n%s' %
                               (tar_path,
                                '  '.join([idir.dname for idir in con.cdirs]) +
                                '  ' +
                                '  '.join([ifile.fname for ifile in con.files]))))
    else:
        write_master_log('client %s: ls %s. No such file or direcotry.' %
                         (addr, tar_path))
        client.send(turn_bytes('ls: %s\nNo such file or directory' % tar_path))
        

def do_mkdir (client, addr):
    """Command: mkdir"""
    tar_path = client.recv(1024).decode('utf-8')
    path_list = split_path(tar_path)
    t, con = check_path(path_list)

    if t == 'file' or t == 'dir':
        write_master_log('client %s: mkdir %s. File exists.' %
                         (addr, tar_path))
        client.send(turn_bytes('mkdir: %s\nFile exists' % tar_path))
    elif str(t).isdigit():
        while t != len(path_list):
            cdir = WfsDir(path_list[t], con)
            cdir.lock_init()
            con.rwlock.write_lock()
            con.cdirs.append(cdir)
            con.rwlock.write_unlock()
            con = cdir
            t += 1
        write_master_log('client %s: mkdir %s. Done.' %
                         (addr, tar_path))
        client.send(turn_bytes('mkdir: %s' % tar_path))
    else:
        write_master_log('client %s: mkdir %s. Wrong request.' %
                         (addr, tar_path))
        client.send(turn_bytes('mkdir: %s\nWrong request' % tar_path))


def do_rmdir (client, addr):
    """Command: rmdir"""
    tar_path = client.recv(1024).decode('utf-8')
    path_list = split_path(tar_path)
    t, con = check_path(path_list)

    if t == 'dir':
        con.rwlock.read_lock()
        if not (con.cdirs or con.files):
            pdir = con.pdir
            con.rwlock.read_unlock()
            pdir.rwlock.write_lock()
            pdir.cdirs.remove(con)
            pdir.rwlock.write_unlock()
            write_master_log('client %s: rmdir %s: Done.' %
                             (addr, tar_path))
            client.send(turn_bytes('rmdir: %s' % tar_path))
        else:
            con.rwlock.read_unlock()
            write_master_log('client %s: rmdir %s: Directory not empty.' %
                             (addr, tar_path))
            client.send(turn_bytes('rmdir: %s\nDirectory not empty' % tar_path))
    elif t == 'file':
        write_master_log('client %s: rmdir %s: Not a directory.' %
                         (addr, tar_path))
        client.send(turn_bytes('rmdir: %s\nNot a directory' % tar_path))
    else:
        write_master_log('client %s: rmdir %s: No such file or directory.' %
                         (addr, tar_path))
        client.send(turn_bytes('rmdir: %s\nNo such file or directory' % tar_path))


def do_mknod (client, addr):
    """Command: mknod"""
    tar_path = client.recv(1024).decode('utf-8')
    path_list = split_path(tar_path)
    t, con = check_path(path_list)

    if not t:
        write_master_log('client %s: mknod %s: No such file or directory' %
                         (addr, tar_path))
        client.send(turn_bytes('mknod: %s\nNo such file or directory' % tar_path))
    elif t == 'dir' or t == 'file':
        write_master_log('client %s: mknod %s: File exists' % (addr, tar_path))
        client.send(turn_bytes('mknod: %s\nFile exists' % tar_path))
    elif str(t).isdigit():
        if t != len(path_list)-1:
            write_master_log('client %s: mknod %s: No such file or directory' %
                             (addr, tar_path))
            client.send(turn_bytes('mknod: %s\nNo such file or directory' %
                                   tar_path))
        else:
            ifile = WfsFile(path_list[-1], con)
            ifile.lock_init()
            con.rwlock.write_lock()
            con.files.append(ifile)
            con.rwlock.write_unlock()
            write_master_log('client %s: mknod %s: Done' % (addr, tar_path))
            client.send(turn_bytes('mknod: %s\n' % tar_path))
    

def do_write(client, addr):
    """Get content and write into file"""
    tar_path = client.recv(1024).decode('utf-8')
    num = client.recv(1024).decode('utf-8')
    path_list = split_path(tar_path)
    t, con = check_path(path_list)

    if t != 'file' or not num.isdigit():
        write_master_log('client %s: write: error' % (addr))
        client.send(turn_bytes('0001'))
        return

    block_size = common_cfg['block_size']
    segs = []
    num = int(num)
    client.send(turn_bytes('1111'))
    for i in range(0, num):
        while True:
            crc = client.recv(32).decode('utf-8')
            seg = client.recv(block_size).decode('utf-8')
            cal = calculate_crc(seg)
            if cal == crc:
                segs.append(seg)
                client.send(turn_bytes('1111'))
                break
            else:
                client.send(turn_bytes('0001'))

    print(segs)
    

