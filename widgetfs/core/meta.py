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
import pickle
from widgetfs.conf.config import common_cfg
from widgetfs.conf.codef import *


class WfsMeta(object):
    root_dir = WfsDir('/', '')
    chunk_list = []


def init_all_locks(ndir):
    ndir.lock_init()
    for idir in ndir.cdirs:
        init_all_locks(idir)
    for ifile in ndir.files:
        ifile.lock_init()


def del_all_locks(ndir):
    ndir.lock_del()
    for idir in ndir.cdirs:
        del_all_locks(idir)
    for ifile in ndir.files:
        ifile.lock_del()


def check_meta():
    """Read meta data from meta file"""
    var_path = common_cfg['var_path']
    fs_meta_file = os.path.normpath(var_path + '/fs.meta')
    chuck_meta_file = os.path.normpath(var_path + '/chunk.meta')
    
    try:
        with open(fs_meta_file, 'rb') as ff:
            WfsMeta.root_dir = pickle.load(ff)
    except FileNotFoundError:
        pass
        
    try:
        with open(chuck_meta_file, 'rb') as ff:
            WfsMeta.chunk_list = pickle.load(ff)
    except FileNotFoundError:
        pass
        
    init_all_locks(WfsMeta.root_dir)


def write_meta():
    """Write meta data to meta file"""
    var_path = common_cfg['var_path']
    fs_meta_file = os.path.normpath(var_path + '/fs.meta')
    chunk_meta_file = os.path.normpath(var_path + '/chunk.meta')

    del_all_locks(WfsMeta.root_dir)
    with open(fs_meta_file, 'wb') as ff:
        pickle.dump(WfsMeta.root_dir, ff)
    with open(chunk_meta_file, 'wb') as ff:
        pickle.dump(WfsMeta.chunk_list, ff)
    
    
