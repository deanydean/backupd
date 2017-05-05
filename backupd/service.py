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

import backup
import daemon.runner
import logging
import os
import sys
import time
import yaml

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
_LOG = logging.getLogger(__name__)

class Service():
    """
        A service that will perform backups at a fixed interval
    """

    def __init__(self, config_file):
        self.config_file = config_file
        self.backup_interval_mins = 1
        self.load_cfg()

    def load_cfg(self):
        # Load the config file
        with open(self.config_file, "r") as yamlfile:
            self.config = yaml.load(yamlfile)

        self.path = self.config["path"]
      
        if "backup_interval_mins" in self.config:
            self.backup_interval_mins = self.config["backup_interval_mins"]

        self.stdin_path = "/dev/null"
        self.stdout_path = os.path.join(self.path, "backupd.log")
        self.stderr_path = self.stdout_path
        self.pidfile_path = os.path.join(self.path, "backupd.pid")
        self.pidfile_timeout = 5

        self.backup_config = []
        if "backups" in self.config:
            self.backup_config = self.config["backups"]

        self.active_backups = []
        for config in self.backup_config:
            self.active_backups.append(backup.Backup(config))

    def run(self):
        _LOG.info("Backupd service started")

        while True:
            try:
                self.load_cfg()

                if len(self.active_backups):
                    _LOG.info("Starting backup")
                    for backup in self.active_backups:
                        _LOG.info("Backing up "+backup.src+" -> "+backup.dst)
                        backup.do_backup_now()
                    _LOG.info("Backup complete")
                else:
                    _LOG.info("No backups configured")
            except IOError as e:
                _LOG.warning("Failed to schedule backup : "+str(e))
            except:
                error = sys.exc_info()[0]
                _LOG.warning("Failed to schedule backup : "+str(error))

            time.sleep(self.backup_interval_mins*60)

        _LOG.info("Backupd service stopped.")

# Get the config file
cd = os.getcwd()
config_file = os.path.join(cd, "backupd.yaml")

if not os.path.exists(config_file):
    _LOG.warning("Cannot find config file "+config_file)
    sys.exit(1)

# Create the main service
service = Service(config_file)

# Control the daemon
daemon_runner = daemon.runner.DaemonRunner(service)
daemon_runner.do_action()
