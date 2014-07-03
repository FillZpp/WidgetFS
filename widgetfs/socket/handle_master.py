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
from widgetfs.conf.config import dserver_cfg, common_cfg
from widgetfs.conf.codef import turn_bytes
from widgetfs.core.log import write_dserver_log
from widgetfs.core.chunk_operation import *
from widgetfs.core.chunk_ctrl import calculate_crc


def handle_master_connection(master):
    """Deal with master commands"""
    ctrl_data = master.recv(4).decode('utf-8')

    if ctrl_data == '0000':
        master.send(turn_bytes('1111'))
    elif ctrl_data == '0001':
        do_create_chunk(master)
    elif ctrl_data == '0010':
        do_write_chunk(master)

    write_dserver_log('Disconnect with master')


def do_create_chunk(master):
    """Create chunk in this data server"""
    master.send(turn_bytes('1111'))
    chid = master.recv(8).decode('utf-8')
    ver = master.recv(4).decode('utf-8')
    
    data_path = dserver_cfg['data_path']
    chunk_path = os.path.normpath(data_path + '/wfs_' + chid + '_' + ver + '.chunk')

    with open(chunk_path, 'w') as ff:
        ff.write(''.join([' ' for i in range(64*1024*1024)]))

    write_dserver_log('master: create new chunk: %s' % chunk_path)
    master.send(turn_bytes('1111'))


def do_write_chunk(master):
    """Get content and write into chunk"""
    master.send(turn_bytes('1111'))
    chid = master.recv(8).decode('utf-8')
    num = int(master.recv(4).decode('utf-8'))
    master.send(turn_bytes('1111'))

    index_list = []
    for i in range(0, num):
        data = int(master.recv(4).decode('utf-8'))
        index_list.append(data)
        master.send(turn_bytes('1111'))

    segs = []
    crcs = []
    for i in range(0, num):
        while True:
            crc = master.recv(32).decode('utf-8')
            seg = master.recv(common_cfg['dataserver_port'])
            cal = calculate_crc(seg)
            if crc == cal:
                segs.append(seg)
                crcs.append(crc)
                master.send(turn_bytes('1111'))
                break
            else:
                master.send(turn_bytes('0001'))

    write_into_chunk_file(chid, index_list, segs, crcs)
    write_dserver_log('master: write into %s chunk: %s' % (chid, str(index_list)))



