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
import time
import threading


master_log = ''
dserver_log = ''
log_lock = threading.Lock()


def get_time_log ():
    nt = time.ctime().split(' ')
    c = nt[3].replace(':', '_')
    return nt[4] + '_' + nt[2] + '_' + c + '.log'


def write_master_log (content):
    if not master_log:
        time_log = 'master_' + get_time_log()
        master_log = os.path.normpath(os.getcwd() + 'log/' + time_log)
    
    log_lock.acquire()
    with open(master_log, 'a') as ff:
        ff.write(time.ctime() + '  ' + content + '\n')
    log_lock.release()


def write_dserver_log (content):
    if not dserver_log:
        time_log = 'dataserver_' + get_time_log()
        dserver_log = os.path.normpath(os.getcwd() + 'log/' + time_log)
        
    log_lock.acquire()
    with open(dserver_log, 'a') as ff:
        ff.write(time.ctime() + '  ' + content + '\n')
    log_lock.release()

    
