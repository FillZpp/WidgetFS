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
from widgetfs.core.meta import write_meta
from widgetfs.core.log import write_master_log
from widgetfs.socket.handle_client import handle_client_connection

if sys.version_info < (3,):
    py_version = 2
else:
    py_version = 3

tcpserver_for_client = socket(AF_INET, SOCK_STREAM)
tcpserver_for_dserver = socket(AF_INET, SOCK_STREAM)

client_port = master_cfg['client_port']
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
        data = self.client.recv(4)
        if data == b'0000':
            write_master_log('Get connection with client %s.' % str(self.addr))
            if py_version == 3:
                data = bytes('1111', 'utf-8')
            else:
                data = '1111'
            self.client.send(data)
            handle_client_connection(self.client, self.addr)
        write_master_log('Not identified client %s.' % str(self.addr))


class ListenClient (threading.Thread):
    """Thread for listening for connection from client"""
    def run (self):
        self.cthreads = []
        try:
            tcpserver_for_client.bind(('', client_port))
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

            
class DserverThread (threading.Thread):
    """Thread for each dserver connection"""
    def __init__ (self, dserver, addr):
        threading.Thread.__init__(self)
        self.dserver = dserver
        self.addr = addr

    def run (self):
        print('get dserver connection %s' % self.addr)


class ListenDserver (threading.Thread):
    """Thread for listening to connection from dserver"""
    def run (self):
        self.dthreads = []
        try:
            tcpserver_for_dserver.bind(('', master_port))
            tcpserver_for_dserver.listen(common_cfg['max_listen'])

            while True:
                dserver, addr = tcpserver_for_dserver.accept()
                if not addr in dserver_slaves:
                    dserver.close()
                    continue
                dthread = DserverThread(dserver, addr)
                dthread.start()
                dthreads.append(dthread)

                for dthread in dthreads:
                    if not dthread.isAlive():
                        dthreads.remove(dthread)
                        dthread.join()
        except error as e:
            sys.stderr.write('Error:\n  error in listen client thread.\n' +
                             e.errno + '  ' + e.strerror)
        

def handle_sigterm (a, b):
    """Handle sigterm
    Close tcp server and exit"""
    tcpserver_for_client.close()
    tcpserver_for_dserver.close()
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

    # start to listen data server
    listen_dserver = ListenDserver()
    listen_dserver.daemon = True
    listen_dserver.start()

    while True:
        time.sleep(10000)
    

