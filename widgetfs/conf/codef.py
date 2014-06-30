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


from widgetfs.conf.rwlock import RWLock

    
class WfsChunk (object):
    """Chunk in Widget file system"""
    def __init__ (self, num, version, ds_list):
        self.num = num
        self.version = version
        self.dserver_list = ds_list
        self.chunk_path = ''


class WfsFile (object):
    """File in Widget file system"""
    def __init__ (self, fname, pdir='/'):
        self.fname = fname
        self.pdir = pdir
        self.size = 0
        self.chunk_dict = {}
        self.rwlock = RWLock()


class WfsDir(object):
    """Directory in Widget file system"""
    def __init__(self, dname, pdir):
        self.dname = dname
        self.pdir = pdir
        self.cdirs = []
        self.files = []
        self.rwlock = RWLock()


