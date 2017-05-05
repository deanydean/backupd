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

import sync

class Backup():
    """
        A backup.
    """

    def __init__(self, config):
        self.src = config["src"]
        self.dst = config["dst"]

        if "rsync_options" in config:
            self.synchronizer = sync.RsyncSynchronizer(config["rsync_options"])
        else:
            self.synchronizer = sync.RsyncSynchronizer()

    def do_backup_now(self):
        """
            Perform the backup now.
        """
        return self.synchronizer.sync(self.src, self.dst)
