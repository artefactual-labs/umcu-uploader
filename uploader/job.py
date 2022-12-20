import inspect
import json
import threading

import sqlite3


# From https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Job(threading.Thread):
    conn = None  # Connection for job management
    __conn = None  # Connection for thread

    params = {}
    default_user_id = "1"
    id = None

    def child_properties(self):
        # Get all attributes
        all_attributes = inspect.getmembers(
            self.__class__, lambda a: not (inspect.isroutine(a))
        )

        # Filter out private attributes
        class_properties = [
            a
            for a in all_attributes
            if not (a[0].startswith("__") and a[0].endswith("__"))
        ]

        # Create dict of remaining attributes and their values
        child_properties = {}

        for class_property in class_properties:
            property_name = class_property[0]

            # Filter out properties from base classes
            if not hasattr(threading.Thread, property_name) and not hasattr(
                Job, property_name
            ):
                child_properties[property_name] = getattr(self, property_name)

        return child_properties

    def new_conn(self):
        return sqlite3.connect("jobs.db")

    def get_conn(self):
        if self.conn is None:
            self.conn = self.new_conn()
        return self.conn

    def begin(self, description):
        # Set user ID
        if self.user_id:
            user_id = str(self.user_id)
        else:
            user_id = self.default_user_id

        self.__conn = self.new_conn()  # Open new connection for thread

        # Create table if needed
        cur = self.__conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS job( \
                id INTEGER PRIMARY KEY, \
                user_id TEXT, \
                job_type TEXT, \
                params TEXT, \
                current_operation TEXT, \
                error TEXT, \
                error_code INTEGER, \
                complete INT, \
                createdatetime TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S:%s', 'now', 'localtime')) \
            )"
        )

        # Note that job has started
        cur.execute(
            "INSERT INTO job \
                (user_id, job_type, params, current_operation, complete) \
                VALUES (?, ?, ?, ?, ?)",
            (user_id, description, json.dumps(self.params), "Working", 0),
        )
        self.__conn.commit()

        self.id = cur.lastrowid

    def error(self, error, error_code=0):
        # Note error
        cur = self.__conn.cursor()
        cur.execute(
            "UPDATE job SET error=?, error_code=?, current_operation='', complete=1 WHERE id=?",
            (
                error,
                error_code,
                self.id,
            ),
        )
        self.__conn.commit()

    def current_operation(self, operation):
        cur = self.__conn.cursor()
        cur.execute(
            "UPDATE job SET current_operation=? WHERE id=?",
            (
                operation,
                self.id,
            ),
        )
        self.__conn.commit()

    def end(self):
        # Mark job as complete
        cur = self.__conn.cursor()
        cur.execute(
            "UPDATE job SET current_operation='', complete=1 WHERE id=?", (self.id,)
        )
        self.__conn.commit()

    def list(self, user_id=None, limit=None):
        # Make returned rows be dicts (with column name as key)
        self.get_conn().row_factory = dict_factory
        cur = self.get_conn().cursor()

        # Assemble limit clause
        limit_clause = ""
        if limit:
            limit_clause = f"LIMIT {limit}"

        if user_id is None:
            res = cur.execute(f"SELECT * FROM job ORDER BY id DESC {limit_clause}")
        else:
            res = cur.execute(
                f"SELECT * FROM job WHERE user_id=? ORDER BY id DESC {limit_clause}",
                (str(user_id),),
            )

        return res.fetchall()

    def get(self, job_id, user_id=None):
        # Make returned rows be dicts (with column name as key)
        self.get_conn().row_factory = dict_factory
        cur = self.get_conn().cursor()

        if user_id is None:
            res = cur.execute(f"SELECT * FROM job WHERE id=?", (str(job_id),))
        else:
            res = cur.execute(
                f"SELECT * FROM job WHERE user_id=? AND id=?",
                (
                    str(user_id),
                    str(job_id),
                ),
            )

        return res.fetchone()

    def clear(self, user_id=None):
        # Clear jobs
        cur = self.get_conn().cursor()

        if user_id is None:
            res = cur.execute("DELETE FROM job")
        else:
            res = cur.execute("DELETE FROM job WHERE user_id=?", (str(user_id),))

        self.conn.commit()

    def do(self):
        self.params = self.child_properties()
        self.start()
