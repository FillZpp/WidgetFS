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
wfs_home_path = os.environ.get('WFS_HOME')
if not wfs_home_path:
    sys.stderr.write('Error:\nYou should define environment variable WFS_HOME first.\n')
    sys.exit(-1)
sys.path.append(wfs_home_path)
import widgetfs.core.config
import widgetfs.core.meta


def daemon_work ():
    # read and check the configuration file
    os.chdir(wfs_home_path)
    with open('etc/wfs_master.cfg') as ff:
        cfg_list = ff.readlines()
    widgetfs.core.config.check_config (cfg_list,
                                       widgetfs.core.config.MasterConfig)


if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write ('Error:\n fork failed: %d (%s)'
                          % (e.errno, e.strerror))
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print ('WidgetFS starts in pid %d' % pid)
            sys.exit(0)
    except OSError, e:
        os.stderr.write ('Error:\n fork failed: %d (%s)'
                         % (e.errno, e.strerror))
        sys.exit(1)

    daemon_work()
    print ('WidgetFS end')


