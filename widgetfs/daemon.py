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
from widgetfs.config import WfsConfig, wfs_check_config
from widgetfs.meta import read_meta


def set_master_pid(var_path):
    pid_dir = os.path.normpath(var_path + 'mrun/')
    pid_file = os.path.normpath(var_path + 'mrun/wfs_master.pid')

    # check if wfs master is running
    try:
        os.mkdir(pid_dir)
    except FileExistsError:
        sys.stderr.write('Error:\nWidgetFS master is already running.\n')
    
    # write in current pid
    pid = str(os.getpid())
    with open(pid_file, 'w') as ff:
        ff.write(pid + '\n')
    print('WidgetFS master starts on pid %s.' % pid)


def set_dserver_pid(var_path):
    pid_dir = os.path.normpath(var_path + 'drun/')
    pid_file = os.path.normpath(var_path + 'drun/wfs_dserver.pid')

    # check if wfs data server is running
    try:
        os.mkdir(pid_dir)
    except FileExistsError:
        sys.stderr.write('Error:\nWidgetFS data server is already running.\n')
    
    # write in current pid
    pid = str(os.getpid())
    with open(pid_file, 'w') as ff:
        ff.write(pid + '\n')
    print('WidgetFS data server starts on pid %s.' % pid)

    

def daemon_work(server):
    # read and check the configuration file
    with open('etc/wfs_master.cfg', 'r') as ff:
        cfg_list = ff.readlines()
    wfs_check_config(cfg_list, WfsConfig.master_cfg)

    var_path = WfsConfig.common_cfg['var_path']
    # create pid file
    if server == 'master':
        set_master_pid(var_path)
    else:
        set_dserver_pid(var_path)

    # read dserver.meta
    root_dir = read_meta(var_path, server)
    
    time.sleep(100)

