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
import time
from widgetfs.conf.config import *
from widgetfs.conf.codef import WfsDir
from widgetfs.core.meta import check_meta
from widgetfs.socket.master_tcp_server import master_tcp_start
from widgetfs.socket.dserver_tcp_server import dserver_tcp_start


def set_master_pid(var_path):
    """Create master pid file and write in pid"""
    pid_dir = os.path.normpath(var_path + 'mrun/')
    pid_file = os.path.normpath(var_path + 'mrun/wfs_master.pid')

    # check if wfs master is running
    try:
        os.mkdir(pid_dir)
    except FileExistsError:
        sys.stderr.write('Error:\n  master server is already running.\n')
    
    # write in current pid
    pid = str(os.getpid())
    with open(pid_file, 'w') as ff:
        ff.write(pid + '\n')
    print('WidgetFS master server starts on pid %s.' % pid)


def set_dserver_pid(var_path):
    """Create data server pid file and write in pid"""
    pid_dir = os.path.normpath(var_path + 'drun/')
    pid_file = os.path.normpath(var_path + 'drun/wfs_dserver.pid')

    # check if wfs data server is running
    try:
        os.mkdir(pid_dir)
    except FileExistsError:
        sys.stderr.write('Error:\n  data server is already running.\n')
    
    # write in current pid
    pid = str(os.getpid())
    with open(pid_file, 'w') as ff:
        ff.write(pid + '\n')
    print('WidgetFS data server starts on pid %s.' % pid)


def daemon_start (server):
    """Entrance of daemon process"""
    var_path = common_cfg['var_path']
    # create pid file
    if server == 'master':
        set_master_pid(var_path)
        check_meta()
        master_tcp_start()
    else:
        set_dserver_pid(var_path)
        dserver_tcp_start()

