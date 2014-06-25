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


class WfsConfig (object):
    """Global configuration for WidgetFS"""
    common_cfg = {
        'chunk_size': 1024*1024*64,
        'block_size': 1024*64,
    }

    master_cfg = {
        'working_user': 'wfs',
        'working_group': 'wfs',

        'client_port': 12180,
        'master_port': 12181,
        'data_port': 12182,
        
        'max_concurrency_visit': 100,
        'pid_file': 'var/run/wfs_master.pid'
    }

    dserver_cfg = {
        'master_host': '',
        'master_port': 12181,
        'master_port': 12182,

        'data_path': '/mnt/wfs',
    }
    

def wfs_check_config (cfg_list, cfg_dict):
    for cfg in cfg_list:
        cfg = cfg.strip()
        if not cfg or cfg[0] == '#':
            continue

        mkey, mvalue = [s.strip() for s in cfg.split('=')]
        if cfg_dict.has_key(mkey):
            g_dict[mkey] = mvalue


