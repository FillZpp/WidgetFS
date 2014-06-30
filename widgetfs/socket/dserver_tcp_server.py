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


import sys
import time
import signal
import threading
from socket import *
from widgetfs.conf.config import common_cfg, dserver_cfg


tcpserver_for_master = socket(AF_INET, SOCK_STREAM)

master_host = dserver_cfg['master_host']
master_port = dserver_cfg['master_port']
dserver_port = dserver_cfg['dataserver_port']


class MasterThread (threading.Thread):
    """Thread for master connection"""
    def __init__ (self, master, addr):
        self.master = master
        self.addr = addr

    def run (self):
        print('get master connection %s' % self.addr)


class ListenMaster (threading.Thread):
    """Thread for listening to connection from master"""
    def run (self):
        self.mthreads = []
        try:
            tcpserver_for_master.bind((master_host, master_port))
            tcpserver_for_master.listen(common_cfg['max_listen'])

            while True:
                master, addr = tcpserver_for_master.accept()
                mthread = MasterThread(master, addr)
                mthread.start()
                mthreads.append(mthread)

                for mthread in mthreads:
                    if not mthread.isAlive():
                        mthreads.remove(mthread)
                        mthread.join()
        except error:
            pass
                

def handle_sigterm (a, b):
    """Handle sigterm
    Close tcp server and exit"""
    tcpserver_for_master.close()
    print('Widget file system stops')
    sys.exit(0)


def dserver_tcp_start ():
    """Loop in data server daemon process"""
    signal.signal(signal.SIGTERM, handle_sigterm)
    
    # start to listen master
    listen_master = ListenMaster()
    listen_master.daemon = True
    listen_master.start()

    while True:
        time.sleep(10000)
    

