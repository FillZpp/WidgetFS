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


class WfsChunk (object):
    """Chunk in Widget file system"""
    def __init__ (self, num, ver, ds_list):
        self.number = num
        self.version = ver
        self.data_server_list = ds_list
        self.chunk_path = get_chunk_path()

    def get_chunk_path(self):
        pass


class WfsFile (object):
    """File in Widget file system"""
    def __init__ (self, fname):
        self.file_name = fname


class WfsDir (object):
    """Directory in Widget file system"""
    def __init__ (self, dname):
        self.dir_name = dname
        
