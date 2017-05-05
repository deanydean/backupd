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

import filecmp
import shutil
import os
import unittest

from backupd import sync

class RsyncSynchronizerTests(unittest.TestCase):
    """
        Unit test for the rsync synchronizer impl
    """

    def setUp(self):
        self.test_dir = ".bud_rsyncsync_ut_tmp"
        self.test_src = "test_src_dir"
        self.test_dst = "test_dst_dir"
        self.test_src_dir = os.path.join(self.test_dir, self.test_src)
        self.test_dst_dir = os.path.join(self.test_dir, self.test_dst)

        if not os.path.exists(self.test_dir):
            # Create the test directory
            os.mkdir(self.test_dir)

            # Create a test src directory
            os.mkdir(self.test_src_dir)

            # Create the dst dir
            os.mkdir(self.test_dst_dir)

        # Create some test src files
        self.test_files = []
        for i in range(0,3):
            # Set the data
            test_file_name = "test_file"+str(i)+".txt"
            test_file_path = os.path.join(self.test_src_dir, test_file_name)
            self.test_files.append({
                "name": test_file_name,
                "path": test_file_path
            })
            
            # Write something to the files
            test_file = open(test_file_path, "w")
            test_file.write("test file "+str(i))
            test_file.close()

    def tearDown(self):
        # Delete the test directory
        shutil.rmtree(self.test_dir)
        pass
    
    def test_syncfile(self):
        """
            Tests that a file can be sync'd
        """
        synchronizer = sync.RsyncSynchronizer()

        src_file = self.test_files[0]["path"]
        dst_file = os.path.join(self.test_dst_dir, self.test_files[0]["name"])

        self.assertTrue(synchronizer.sync(src_file, dst_file)) 
        self.assertTrue(filecmp.cmp(src_file, dst_file))

    def test_syncdir(self):
        """
            Tests that a directory can be sync'd
        """
        synchronizer = sync.RsyncSynchronizer()

        src_dir = self.test_src_dir
        dst_dir = self.test_dst_dir

        # Sync the directories
        self.assertTrue(synchronizer.sync(src_dir, dst_dir))

        # Compare the files in the directories
        dst_dir = os.path.join(self.test_dst_dir, self.test_src)
        files = map(lambda i: i["name"], self.test_files)
        match, mismatch, err = filecmp.cmpfiles(src_dir, dst_dir, files)

        for f in files: 
            self.assertIn(f, match)
        self.assertTrue(not mismatch)
        self.assertTrue(not err)

    def test_syncfiletomissingdir(self):
        """
            Tests that a file can be sync'd to a directory that's missing
        """
        synchronizer = sync.RsyncSynchronizer()

        new_dir = os.path.join("missing_dir", ".")
        src_file = self.test_files[0]["path"]
        dst_dir = os.path.join(self.test_dst_dir, new_dir)

        # Sync the file to the missing directory (should fail)
        self.assertFalse(synchronizer.sync(src_file, dst_dir))
        
    def test_syncwithoptions(self):
        """
            Tests that options provided to the synchronizer are effective
        """
        options = "--dry-run"
        synchronizer = sync.RsyncSynchronizer(options)

        src_file = self.test_files[0]["path"]
        dst_file = os.path.join(self.test_dst_dir, self.test_files[0]["name"])

        # Do the sync (it should succeed)
        self.assertTrue(synchronizer.sync(src_file, dst_file)) 
        
        # Make sure the dst file does not exist
        self.assertFalse(os.path.exists(dst_file))

    def test_manyfilesyncs(self):
        """
            Tests that a single synchronizer can do many syncs
        """
        synchronizer = sync.RsyncSynchronizer()

        src_dir = self.test_src_dir
        dst_dir = self.test_dst_dir

        # Sync each test file
        for f in self.test_files:
            dst_file = os.path.join(dst_dir, f["name"])
            self.assertTrue(synchronizer.sync(f["path"], dst_file))

        # Compare the files in the directories
        files = map(lambda i: i["name"], self.test_files)
        match, mismatch, err = filecmp.cmpfiles(src_dir, dst_dir, files)

        for f in files: 
            self.assertIn(f, match)
        self.assertTrue(not mismatch)
        self.assertTrue(not err)

        pass
