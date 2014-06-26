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
    sys.stderr.write('Error:\n  ' +
                     'You should define environment variable WFS_HOME first.\n')
    sys.exit(-1)
sys.path.append(wfs_home_path)
from widgetfs.daemon import daemon_start, daemon_stop


def print_help ():
    """Print wfs_master help"""
    print('Widget file system master server.\n' +
          'Usage: [start | stop]')


def master_start ():
    """Start master daemon process
    Fork twice"""
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('Error:\n  data server fork 1 failed: %d (%s).\n'
                         % (e.errno, e.strerror))
        sys.exit(1)

    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        os.stderr.write('Error:\n  data server fork 2 failed: %d (%s).\n'
                        % (e.errno, e.strerror))
        sys.exit(1)

    daemon_start('master')


def master_stop ():
    """ Stop master daemon process
    Remove pid file and send sigterm to master daemon process"""
    var_path = daemon_stop('master')
    pid_dir = os.path.normpath(var_path + 'mrun/')
    pid_file = os.path.normpath(var_path + 'mrun/wfs_master.pid')
    
    # read and check pid file
    if not os.path.isfile(pid_file):
        sys.stderr.write('Error:\n  No running WidgetFS master.\n')
        sys.exit(-1)

    with open(pid_file, 'r') as ff:
        pid = ff.readline()

    os.remove(pid_file)
    os.rmdir(pid_dir)
    os.kill(int(pid), signal.SIGTERM)


def main ():
    """Check parameters"""
    os.chdir(wfs_home_path)

    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            master_start()
        elif sys.argv[1] == 'stop':
            master_stop()
    else:
        print_help()


if __name__ == '__main__':
    main()

