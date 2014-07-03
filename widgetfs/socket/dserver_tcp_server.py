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
import signal
import threading
from socket import *
from widgetfs.conf.config import common_cfg, dserver_cfg
from widgetfs.conf.codef import turn_bytes
from widgetfs.core.log import write_dserver_log
from widgetfs.socket.handle_master import *


tcpserver_for_master = socket(AF_INET, SOCK_STREAM)

master_host = dserver_cfg['master_host']
dserver_port = dserver_cfg['dataserver_port']


class MasterThread (threading.Thread):
    """Thread for master connection"""
    def __init__ (self, master, addr):
        threading.Thread.__init__(self)
        self.master = master
        self.addr = addr

    def run (self):
        data = self.master.recv(4).decode('utf-8')
        if data == '0000':
            write_dserver_log('Get connection with master')
            self.master.send(turn_bytes('1111'))
            handle_master_connection(self.master)
        else:
            write_dserver_log('Not identified message from master')

        self.master.close()


class ListenMaster (threading.Thread):
    """Thread for listening to connection from master"""
    def run (self):
        self.mthreads = []
        try:
            tcpserver_for_master.bind(('', dserver_port))
            tcpserver_for_master.listen(common_cfg['max_listen'])
            while True:
                master, addr = tcpserver_for_master.accept()
                mthread = MasterThread(master, addr)
                mthread.start()
                self.mthreads.append(mthread)

                for mthread in self.mthreads:
                    if not mthread.isAlive():
                        self.mthreads.remove(mthread)
                        mthread.join()
        except error:
            sys.stderr.write('Error:\n  error in listen master thread.\n' +
                             e.errno + '  ' + e.strerror)
                

def handle_sigterm (a, b):
    """Handle sigterm
    Close tcp server and exit"""
    tcpserver_for_master.close()
    print('Widget file system stops')
    sys.exit(0)


def dserver_tcp_start ():
    """Loop in data server daemon process"""
    signal.signal(signal.SIGTERM, handle_sigterm)

    data_path = dserver_cfg['data_path']
    if not os.path.isdir(data_path):
        try:
            os.mkdir(data_path)
        except PermissionError as e:
            sys.stderr.write('Error:\n' + e.strerror + '\n')
            sys.exit(1)
    
    # start to listen master
    listen_master = ListenMaster()
    listen_master.daemon = True
    listen_master.start()

    while True:
        time.sleep(10000)
    

