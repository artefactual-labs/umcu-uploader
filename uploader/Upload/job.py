import json
import os
import shutil
import threading

import sqlite3

from uploader.Metadata import DATAVERSE_METADATA_FILENAME
from uploader.Metadata import arc_metadata
from uploader.Metadata.arc_metadata import METADATA_FILENAME


class Job(threading.Thread):
    conn = None  # Connection for job management
    __conn = None  # Connection for thread

    params = {}
    default_user_id = 1
    id = None

    def params(self, params):
        self.params = params

    def new_conn(self):
        return sqlite3.connect("jobs.db")

    def get_conn(self):
        if self.conn is None:
            self.conn = self.new_conn()
        return self.conn

    def begin(self, job_type, job_params):
        # Set user ID
        if "user_id" in job_params:
            user_id = job_params["user_id"]
        else:
            user_id = self.default_user_id

        self.__conn = self.new_conn()  # Open new connection for thread

        # Create table if needed
        cur = self.__conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS job( \
                id INTEGER PRIMARY KEY, \
                user_id INTEGER, \
                job_type TEXT, \
                params TEXT, \
                complete INT \
            )"
        )

        # Note that job has started
        cur.execute(
            "INSERT INTO job \
                (user_id, job_type, params, complete) \
                VALUES (?, ?, ?, ?)",
            (user_id, job_type, json.dumps(job_params), 0),
        )
        self.__conn.commit()

        self.id = cur.lastrowid

    def end(self):
        # Mark job as complete
        cur = self.__conn.cursor()
        cur.execute("UPDATE job SET complete=1 WHERE id=?", (self.id,))
        self.__conn.commit()

    def list(self, user_id=None):
        # Return list of jobs
        cur = self.get_conn().cursor()

        if user_id is None:
            res = cur.execute("SELECT * FROM job")
        else:
            res = cur.execute("SELECT * FROM job WHERE user_id=?", (user_id,))

        return res.fetchall()

    def clear(self, user_id=None):
        # Clear jobs
        cur = self.get_conn().cursor()

        if user_id is None:
            res = cur.execute("DELETE FROM job")
        else:
            res = cur.execute("DELETE FROM job WHERE user_id=?", (user_id,))

        self.conn.commit()
        #TODO: find whether returning res makes sense, res is currently a unaccessible object


class CreateTransferJob(Job):
    #NOTE: instead of params object why not have self.form, self.permissions, self.path, self.destination?
    def run(self):
        super().begin("copy", self.params)
        # Copy transfer files to transfer source location
        shutil.copytree(self.params["source"], self.params["destination"])

        # Create metadata directory if need be
        metadata_directory = os.path.join(self.params["destination"], "metadata")

        if not os.path.isdir(metadata_directory):
            os.mkdir(metadata_directory)

        # Move main metadata file, if it exists, to metadata directory
        main_metadata_filepath = os.path.join(self.params["destination"], DATAVERSE_METADATA_FILENAME)

        if os.path.isfile(main_metadata_filepath):
            shutil.copy(main_metadata_filepath, metadata_directory)
            os.remove(main_metadata_filepath)

        # Get file archivematica metadata file, if it exists, to metadata directory
        archivematica_metadata_filepath = os.path.join(self.params["destination"], METADATA_FILENAME)
        
        # create archivematica metadata file
        arc_metadata.create_metadata(self.params["form"], self.params["permissions"])
        # Move main metadata file, if it exists, to metadata directory
        if os.path.isfile(archivematica_metadata_filepath):
            shutil.copy(archivematica_metadata_filepath, metadata_directory)
            os.remove(archivematica_metadata_filepath)
        
        # TODO: This needs to be updated to use the permissions object
        super().end()
