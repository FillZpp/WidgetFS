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
    sys.stderr.write('Error:\n' +
                     'You should define environment variable WFS_HOME first.\n')
    sys.exit(-1)
sys.path.append(wfs_home_path)
from widgetfs.daemon.master_daemon import daemon_work


def main ():
    os.chdir(wfs_home_path)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('Error:\n fork failed: %d (%s).\n'
                         % (e.errno, e.strerror))
        sys.exit(1)

    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        os.stderr.write('Error:\n fork failed: %d (%s).\n'
                        % (e.errno, e.strerror))
        sys.exit(1)

    daemon_work()
    print('WidgetFS master end.')


if __name__ == '__main__':
    main()

