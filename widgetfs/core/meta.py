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


class WfsRoot(object):
    root_dir = WfsDir('/', '')


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
    meta_file = os.path.normpath(var_path + '/master.meta')
    try:
        with open(meta_file, 'rb') as ff:
            WfsRoot.root_dir = pickle.load(ff)
    except FileNotFoundError:
        pass
        
    init_all_locks(WfsRoot.root_dir)


def write_meta():
    """Write meta data to meta file"""
    var_path = common_cfg['var_path']
    meta_file = os.path.normpath(var_path + '/master.meta')

    del_all_locks(WfsRoot.root_dir)
    with open(meta_file, 'wb') as ff:
        pickle.dump(WfsRoot.root_dir, ff)
    
    
