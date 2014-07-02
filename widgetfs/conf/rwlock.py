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

    
from threading import Lock


class RWLock (object):
    """Read and write lock"""
    def __init__ (self):
        self.rw_lock = Lock()
        self.r_lock = Lock()
        self.nr_lock = Lock()
        self.read_count = 0

    def read_lock (self):
        self.rw_lock.acquire()
        self.r_lock.acquire()

        self.read_count += 1
        if self.read_count == 1:
            self.nr_lock.acquire()

        self.r_lock.release()
        self.rw_lock.release()

    def read_unlock (self):
        self.r_lock.acquire()
        self.read_count -= 1
        if self.read_count == 0:
            self.nr_lock.release()
        self.r_lock.release()

    def write_lock (self):
        self.rw_lock.acquire()
        self.nr_lock.acquire()

    def write_unlock (self):
        self.nr_lock.release()
        self.rw_lock.release()


    
