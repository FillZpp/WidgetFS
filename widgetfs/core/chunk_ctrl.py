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


import string
import random
import threading
from socket import *
from binascii import crc32
from widgetfs.conf.config import master_cfg, common_cfg
from widgetfs.conf.codef import WfsChunk, turn_bytes
from widgetfs.core.meta import WfsMeta


def calculate_crc(content):
    """Calculate crc32 from a content"""
    c = crc32(turn_bytes(content))
    c = crc32(turn_bytes(content), c) & 0xffffffff
    return bin(c).lstrip('0b')


def add_new_chunk():
    """Create new chunk in Widget file system"""
    WfsMeta.rwlock.write_lock()
    judge = True
    while judge:
        judge = False
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        for chunk in WfsMeta.chunk_list:
            if salt == chunk.chid:
                judge = True
                break

    new_chunk = WfsChunk(salt, '1')
    new_chunk.lock_init()
    WfsMeta.chunk_list.append(new_chunk)
    WfsMeta.rwlock.write_unlock()


def get_pos_chunks(num):
    """Get chunks for num blocks"""
    record = []
    index = 0
    count = 0
    while True:
        if len(WfsMeta.chunk_list) == index:
            add_new_chunk()
            
        WfsMeta.rwlock.read_lock()
        chunk = WfsMeta.chunk_list[index]
        blocks_list = []
        blocks_list.append(index)
        
        chunk.rwlock.write_lock()
        for i in range(0, 1000):
            if chunk.blocks[i] == 0:
                chunk.blocks[i] = 1
                blocks_list.append(i)
                count += 1
            if count == num or len(blocks_list) == 4:
                break
        chunk.rwlock.write_unlock()
        WfsMeta.rwlock.read_unlock()

        if len(blocks_list) > 1:
            record.append(tuple(blocks_list))
        if count == num:
            break
        index += 1
            
    return record


class PushToChunk(threading.Thread):
    """Thread for saving content to chunk"""
    def __init__(self, chunk_index, blocks_tuple, segs, crcs):
        threading.Thread.__init__(self)
        self.chunk_index = chunk_index
        self.blocks_tuple = blocks_tuple
        self.segs = segs
        self.crcs = crcs
        

    def run(self):
        chunk = WfsMeta.chunk_list[self.chunk_index]
        chunk.rwlock.write_lock()

        slave = self.check_chunk()
        if not slave:
            print('Error:\nNo running data server for this chunk')
            return

        tcp_dserver = socket(AF_INET, SOCK_STREAM)
        try:
            tcp_dserver.connect((slave, master_cfg['dataserver_port']))
            tcp_dserver.send(turn_bytes('0000'))
            recv = tcp_dserver.recv(4).decode('utf-8')
            tcp_dserver.send(turn_bytes('0011'))
            recv = tcp_dserver.recv(4).decode('utf-8')

            blocks_num = len(self.blocks_tuple)
            tcp_dserver.send(turn_bytes(chunk.chid))
            tcp_dserver.send(turn_bytes(str(blocks_num)))
            tcp_dserver.recv(4).decode('utf-8')
                                             
            for i in range(0, blocks_num):
                tcp_dserver.send(turn_bytes(str(self.blocks_tuple[i])))
                recv = tcp_dserver.recv(4).decode('utf-8')

            for i in range(0, blocks_num):
                while True:
                    tcp_dserver.send(turn_bytes(self.crcs[i]))
                    tcp_dserver.send(turn_bytes(self.segs[i]))
                    recv = tcp_dserver.recv(4).decode('utf-8')
                    if recv == '1111':
                        break
            
        except error as e:
            print('Error:\nConnect to data server: %s' % e.strerror)
        tcp_dserver.close()
        chunk.rwlock.write_unlock()

    def check_chunk(self):
        chunk = WfsMeta.chunk_list[self.chunk_index]
        dserver_num = len(chunk.dserver_list)

        if dserver_num < 3:
            self.set_new_dserver(3 - dserver_num)

        tcp_dserver = socket(AF_INET, SOCK_STREAM)
        for slave in chunk.dserver_list:
            tcp_dserver.connect((slave, master_cfg['dataserver_port']))
            tcp_dserver.send(turn_bytes('0000'))
            recv = tcp_dserver.recv(4).decode('utf-8')
            if recv != '1111':
                continue
            tcp_dserver.send(turn_bytes('0000'))
            recv = tcp_dserver.recv(4).decode('utf-8')
            tcp_dserver.close()
            if recv == '1111':
                return slave

        return None

    def set_new_dserver(self, push_num):
        num = 0
        chunk = WfsMeta.chunk_list[self.chunk_index]

        tcp_dserver = socket(AF_INET, SOCK_STREAM)
        for slave in master_cfg['slaves']:
            if slave in chunk.dserver_list:
                continue
            try:
                tcp_dserver.connect((slave, master_cfg['dataserver_port']))
                tcp_dserver.send(turn_bytes('0000'))
                recv = tcp_dserver.recv(4).decode('utf-8')
                if recv != '1111':
                    tcp_dserver.close()
                    continue
                tcp_dserver.send(turn_bytes('0001'))
                recv = tcp_dserver.recv(4).decode('utf-8')
                
                tcp_dserver.send(turn_bytes(chunk.chid))
                tcp_dserver.send(turn_bytes(chunk.version))
                recv = tcp_dserver.recv(4).decode('utf-8')
                if recv == '1111':
                    chunk.dserver_list.append(slave)
                    num += 1
            except error as e:
                pass
                
            tcp_dserver.close()
            if num == push_num:
                break


class PullFromChunk(object):
    """Pull content from chunks"""
    def __init__(self, pos_chunks, chunk_seq):
        self.pos_chunks = pos_chunks
        self.chunk_seq = chunk_seq

    def get_content(self):
        block_size = common_cfg['block_size']
        all_segs = [[] for i in self.chunk_seq]
        for pos_chunk in self.pos_chunks:
            segs = ['' for i in self.chunk_seq]
            num = len(pos_chunk) - 1
            slave = self.check_chunk(pos_chunk[0])
            if not slave:
                return None
                
            tcp_dserver = socket(AF_INET, SOCK_STREAM)
            tcp_dserver.connect((slave, master_cfg['dataserver_port']))
            tcp_dserver.send(turn_bytes('0000'))
            recv = tcp_dserver.recv(4).decode('utf-8')
            tcp_dserver.send(turn_bytes('0010'))
            recv = tcp_dserver.recv(4).decode('utf-8')

            tcp_dserver.send(turn_bytes(pos_chunk[0].chid))
            tcp_dserver.send(turn_bytes(str(num)))
            recv = tcp_dserver.recv(4).decode('utf-8')

            for i in range(0, num):
                tcp_dserver.send(turn_bytes(str(pos_chunk[i+1])))
                recv = tcp_dserver.recv(4).decode('utf-8')

            tcp_dserver.send(turn_bytes('1111'))
            for i in range(0, num):
                data = tcp_dserver.recv(block_size).decode('utf-8')
                segs.append(data)
                tcp_dserver.send(turn_bytes('1111'))

            for k, v in self.chunk_seq.items():
                if v == pos_chunk[0].chid:
                    all_segs[k-1] = segs

        return all_segs
            


    def check_chunk(self, chunk):
        tcp_dserver = socket(AF_INET, SOCK_STREAM)
        for slave in chunk.dserver_list:
            tcp_dserver.connect((slave, master_cfg['dataserver_port']))
            tcp_dserver.send(turn_bytes('0000'))
            recv = tcp_dserver.recv(4).decode('utf-8')
            if recv != '1111':
                continue
            tcp_dserver.send(turn_bytes('0000'))
            recv = tcp_dserver.recv(4).decode('utf-8')
            tcp_dserver.close()
            if recv == '1111':
                return slave
        return None

        
                
    
