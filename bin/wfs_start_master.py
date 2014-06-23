#! /usr/bin/env python

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
import ctypes
wfs_home_path = os.environ.get('WFS_HOME')
if not wfs_home_path:
    sys.stderr.write('Error:\n' +
                     'You should define environment variable WFS_HOME first.\n')
    sys.exit(-1)
sys.path.append(wfs_home_path)
import widgetfs.core.config
import widgetfs.core.meta


pid_file = 'var/run/widgetfs.pid'


def set_run_pid ():
    try:
        os.mknod (pid_file)
    except OSError, e:
        print e.errno, e.strerror
        sys.stderr.write ('Error:\nWidgetFS is already running.\n')
        sys.exit(-1)
    pid = str(os.getpid()) + '\n'
    with open(pid_file, 'w') as ff:
        ff.write(pid)


def daemon_work ():
    os.chdir(wfs_home_path)
    set_run_pid()
    # read and check the configuration file
    with open('etc/wfs_master.cfg') as ff:
        cfg_list = ff.readlines()
    widgetfs.core.config.check_config (cfg_list,
                                       widgetfs.core.config.MasterConfig)

    time.sleep(20)
    os.remove(pid_file)
    

if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write ('Error:\n fork failed: %d (%s).\n'
                          % (e.errno, e.strerror))
        sys.exit(1)

    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            print ('WidgetFS starts in pid %d.' % pid)
            sys.exit(0)
    except OSError, e:
        os.stderr.write ('Error:\n fork failed: %d (%s).\n'
                         % (e.errno, e.strerror))
        sys.exit(1)

    daemon_work()
    print ('WidgetFS end')


