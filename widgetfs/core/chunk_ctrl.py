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


from binascii import crc32
from widgetfs.conf.codef import WfsDserver, WfsChunk, turn_bytes
from widgetfs.core.meta import WfsMeta


def calculate_crc(content):
    c = crc32(turn_bytes(content))
    c = crc32(turn_bytes(content), c) & 0xffffffff
    return bin(c).lstrip('0b')


def get_block_for_file(n):
    record = []
    
