#!/usr/bin/python
# 
# Copyright 2017 Matt Dean
#
# This file is part of backupd
#
# backupd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# backupd is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with 
# backupd.  If not, see <http://www.gnu.org/licenses/>.

import logging
import subprocess

class Synchronizer():
    """
        A synchronizer is an object that can keep a source and destination in
        sync.
    """

    def sync(self, src, dst):
        """
            Synchronize dst with src
        """
        pass

class RsyncSynchronizer(Synchronizer):
    """
        A synchronizer that uses the rsync command to synchronize files and
        directories.
    """
    
    def __init__(self, cmd_options="--archive"):
        self.rsync_cmd = "rsync"
        self.rsync_options = cmd_options

    def sync(self, src_path, dst_path):
        args = [ self.rsync_cmd, self.rsync_options, src_path, dst_path ]
        logging.debug("Calling "+str(args)+"....")
        ret = subprocess.call(args)

        if ret is 0:
            return True
        else:
            logging.warning("Failed to sync "+src_path+" -> "+dst_path)
            return False
