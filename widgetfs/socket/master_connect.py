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
from widgetfs.config import common_cfg, master_cfg


tcpserver_for_client = socket(AF_INET, SOCK_STREAM)
tcpserver_for_dserver = socket(AF_INET, SOCK_STREAM)

client_port = master_cfg['client_port']
master_port = master_cfg['master_port']
dserver_port = master_cfg['dataserver_port']


class ClientThread (threading.Thread):
    """Thread for each client connect"""
    def __init__ (self, client, addr):
        self.client = client
        self.addr = addr

    def run (self):
        print('get client connect %s' % self.addr)


class ClientListen (threading.Thread):
    """Thread for listening for connection from client"""
    def run (self):
        self.cthreads = []
        try:
            tcpserver_for_client.bind(('', client_port))
            tcpserver_for_client.listen(master_cfg['max_listen'])

            while True:
                client, addr = tcpserver_for_client.accept()
                cthread = ClientThread(client, addr)
                cthread.start()
                cthreads.append(cthread)

                for cthread in cthreads:
                    if not cthread.isAlive():
                        cthreads.remove(cthread)
                        cthread.join()
        except error:
            pass


class DserverThread (threading.Thread):
    """Thread for each dserver connect"""
    def __init__ (self, dserver, addr):
        self.dserver = dserver
        self.addr = addr

    def run (self):
        print('get dserver connect %s' % self.addr)


class DserverListen (threading.Thread):
    """Thread for listening for connection from dserver"""
    def run (self):
        self.dthreads = []
        try:
            tcpserver_for_dserver.bind(('', master_port))
            tcpserver_for_dserver.listen(master_cfg['max_listen'])

            while True:
                dserver, addr = tcpserver_for_dserver.accept()
                dthread = DserverThread(dserver, addr)
                dthread.start()
                dthreads.append(dthread)

                for dthread in dthreads:
                    if not dthread.isAlive():
                        dthreads.remove(dthread)
                        dthread.join()
        except error:
            pass
        

def handle_sigterm (a, b):
    """Handle sigterm
    Close tcp server and exit"""
    tcpserver_for_client.close()
    tcpserver_for_dserver.close()
    print('Widget file system stops.')
    sys.exit(0)


def master_tcp_start ():
    """Loop in master daemon process"""
    signal.signal(signal.SIGTERM, handle_sigterm)

    # start to listen client
    client_listen = ClientListen()
    client_listen.daemon = True
    client_listen.start()

    # start to listen data server
    dserver_listen = DserverListen()
    dserver_listen.daemon = True
    dserver_listen.start()

    while True:
        time.sleep(10000)
    

