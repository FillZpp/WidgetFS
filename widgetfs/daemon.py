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
from widgetfs.core.config import *
from widgetfs.core.meta import read_meta
from widgetfs.socket.master_connect import master_tcp_start
from widgetfs.socket.dserver_connect import dserver_tcp_start


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


def read_cfg (server):
    """Read config file """
    # read and check the configuration file
    if server == 'master':
        with open('etc/wfs_master.cfg', 'r') as ff:
            cfg_list = ff.readlines()
        wfs_check_config(cfg_list, master_cfg)
        with open('etc/wfs_slaves.cfg', 'r') as ff:
            cfg_list = ff.readlines()
        wfs_check_slaves(cfg_list)
    else:
        with open('etc/wfs_dataserver.cfg', 'r') as ff:
            cfg_list = ff.readlines()
        wfs_check_config(cfg_list, dserver_cfg)
    

def daemon_start (server):
    """Entrance of daemon process"""
    read_cfg(server)
    var_path = common_cfg['var_path']
    # create pid file
    if server == 'master':
        set_master_pid(var_path)
        # read meta data from dataserver.meta
        root_dir = read_meta(server)
        master_tcp_start(root_dir)
    else:
        set_dserver_pid(var_path)
        # read meta data from master.meta
        
        dserver_tcp_start()


def daemon_stop (server):
    """Stop of daemon"""
    read_cfg(server)
    var_path = common_cfg['var_path']
    return var_path

