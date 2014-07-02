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


from socket import *


common_cfg = {
    'chunk_size': 1024*1024*64,
    'block_size': 1024*64,
    'var_path': 'var/',
    'max_listen': 100,
}

master_cfg = {
    'master_port': 12180,
    'dataserver_port': 12181,

    'slaves': [],
}

dserver_cfg = {
    'master_host': '',
    'dataserver_port': 12181,
    
    'data_path': '/mnt/wfs',
}
    

def check_config (cfg_list, cfg_dict):
    """Check user's config list"""
    for cfg in cfg_list:
        cfg = cfg.strip()
        if not cfg or cfg.startswith('#'):
            continue

        mkey, mvalue = [s.strip() for s in cfg.split('=')]
        if cfg_dict.has_key(mkey):
            if mkey.endswith('port'):
                mvalue = int(mvalue)
            g_dict[mkey] = mvalue


def check_slaves (slaves_list):
    """Check slaves"""
    for slave in slaves_list:
        slave = slave.strip()
        if not slave or slave.startswith('#'):
            continue

        slave = gethostbyname(slave)
        master_cfg['slaves'].append(slave)


