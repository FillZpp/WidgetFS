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
from widgetfs.core.config import WfsConfig, wfs_check_config


def main ():
    os.chdir(wfs_home_path)

    # read and check the configuration file
    with open('etc/wfs_master.cfg') as ff:
        cfg_list = ff.readlines()
    wfs_check_config(cfg_list, WfsConfig.master_cfg)

    var_path = WfsConfig.common_cfg['var_path']
    pid_dir = os.path.normpath(var_path + 'mrun/')
    pid_file = os.path.normpath(var_path + 'mrun/wfs_master.pid')
    
    # read and check pid file
    if not os.path.isfile(pid_file):
        sys.stderr.write('Error:\nNo running WidgetFS master.\n')
        sys.exit(-1)

    with open(pid_file, 'r') as ff:
        pid = ff.readline()

    os.remove(pid_file)
    os.rmdir(pid_dir)
    os.kill(int(pid), signal.SIGKILL)


if __name__ == '__main__':
    main()



