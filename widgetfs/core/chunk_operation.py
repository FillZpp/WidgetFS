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
from widgetfs.conf.config import common_cfg, dserver_cfg


def write_into_chunk_file(chid, index_list, segs, crcs):
    block_size = common_cfg['block_size']
    data_path = dserver_cfg['data_path']
    chunk_file = ''
    try:
        file_list = os.listdir(data_path)
        for cfile in file_list:
            spl = cfile.split('_')
            if len(spl) > 2 and spl[1] == chid:
                chunk_file = cfile
                break
    except FileNotFoundError as e:
        print('Error:\nCan not find data path')

    chunk_path = os.path.normpath(data_path + '/' + chunk_file)
    with open(chunk_path, 'r') as ff:
        conl = ff.readlines()

    content = ''.join(conl)
    count = 0
    for i in index_list:
        crc_start = block_size*10 + 32*i
        block_start = block_size*(20 + i)
        content = content[:crc_start] + crcs[count] + \
                  content[crc_start+len(crc[count]):block_start] + segs[count] +\
                  content[block_start+len(segs[count]):]
        count += 1

    with open(chunk_path, 'w') as ff:
        ff.write(content)

    
