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


class MasterConfig (object):
    """Global configuration for master"""
    config_dict = {
        "working_user": "wfs",
        "working_group": "wfs",

        "customer_port": 12180,
        "master_port": 12181,
        "data_port": 12182,
        
        "max_concurrency_visit": 100
    }


class DataConfig (object):
    """Global configuration for data server"""
    config_dist = {
        "working_user": "wfs",
        "working_group": "wfs",

        "master_port": 12181,
        "master_port": 12182,
    }


