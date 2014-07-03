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
from widgetfs.conf.config import common_cfg, master_cfg
from widgetfs.conf.codef import turn_bytes
from widgetfs.core.meta import write_meta
from widgetfs.core.log import write_master_log
from widgetfs.socket.handle_client import handle_client_connection


tcpserver_for_client = socket(AF_INET, SOCK_STREAM)
tcpserver_for_dserver = socket(AF_INET, SOCK_STREAM)

master_port = master_cfg['master_port']
dserver_port = master_cfg['dataserver_port']
dserver_slaves = master_cfg['slaves']


class ClientThread (threading.Thread):
    """Thread for each client connect"""
    def __init__ (self, client, addr):
        threading.Thread.__init__(self)
        self.client = client
        self.addr = addr

    def run (self):
        data = self.client.recv(4).decode('utf-8')
        if data == '0000':
            write_master_log('Get connection with client %s.' % str(self.addr))
            self.client.send(turn_bytes('1111'))
            handle_client_connection(self.client, self.addr)
        else:
            write_master_log('Not identified client %s.' % str(self.addr))
            
        self.client.close()


class ListenClient (threading.Thread):
    """Thread for listening for connection from client"""
    def run (self):
        self.cthreads = []
        try:
            tcpserver_for_client.bind(('', master_port))

            tcpserver_for_client.listen(common_cfg['max_listen'])
            while True:
                client, addr = tcpserver_for_client.accept()
                cthread = ClientThread(client, addr)
                cthread.start()
                self.cthreads.append(cthread)

                for cthread in self.cthreads:
                    if not cthread.isAlive():
                        self.cthreads.remove(cthread)
                        cthread.join()
        except error as e:
            sys.stderr.write('Error:\n  error in listen client thread.\n' +
                             e.errno + '  ' + e.strerror)


def handle_sigterm (a, b):
    """Handle sigterm
    Close tcp server and exit"""
    tcpserver_for_client.close()
    write_meta()
    
    print('Widget file system stops.')
    sys.exit(0)


def master_tcp_start ():
    """Loop in master daemon process"""
    signal.signal(signal.SIGTERM, handle_sigterm)

    # start to listen client
    listen_client = ListenClient()
    listen_client.daemon = True
    listen_client.start()

    while True:
        time.sleep(10000)
    

