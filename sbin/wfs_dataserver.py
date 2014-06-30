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
import signal
wfs_home_path = os.environ.get('WFS_HOME')
if not wfs_home_path:
    sys.stderr.write('Error:\n' +
                     'You should define environment variable WFS_HOME first.\n')
    sys.exit(-1)
sys.path.append(wfs_home_path)
os.chdir(wfs_home_path)
from widgetfs.conf.config import common_cfg, dserver_cfg, check_config
from widgetfs.core.daemon import daemon_start


def print_help ():
    """Print wfs_dataserver help"""
    print('Widget file system data server.\n' +
          'Usage: [start | stop]')


def read_cfg():
    """Read config file"""
    with open('etc/wfs_dataserver.cfg', 'r') as ff:
        cfg_list = ff.readlines()
    check_config(cfg_list, dserver_cfg)


def dserver_start ():
    """Start data server daemon process
    Fork twice"""
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('Error:\n  master server fork 1 failed: %d (%s).\n'
                         % (e.errno, e.strerror))
        sys.exit(1)

    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        os.stderr.write('Error:\n  master server fork 2 failed: %d (%s).\n'
                        % (e.errno, e.strerror))
        sys.exit(1)

    read_cfg()
    daemon_start('dserver')


def dserver_stop ():
    """Stop data server daemon process
    Remove pid file and send sigterm to data server daemon process"""
    read_cfg()
    var_path = dserver_cfg['var_path']
    pid_dir = os.path.normpath(var_path + 'drun/')
    pid_file = os.path.normpath(var_path + 'drun/wfs_dserver.pid')
    
    # read and check pid file
    if not os.path.isfile(pid_file):
        sys.stderr.write('Error:\n  No running WidgetFS data server.\n')
        sys.exit(-1)

    with open(pid_file, 'r') as ff:
        pid = ff.readline()

    os.remove(pid_file)
    os.rmdir(pid_dir)
    os.kill(int(pid), signal.SIGTERM)


def main ():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            dserver_start()
        elif sys.argv[1] == 'stop':
            dserver_stop()
    else:
        print_help()


if __name__ == '__main__':
    main()
