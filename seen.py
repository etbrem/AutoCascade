import sys
import os
MAIN_DIRECTORY = os.path.dirname(__file__)
sys.path.append(MAIN_DIRECTORY)
from auto_cascade import *

import json


class DBCommunication(MyAbstractClass):
    abstract_methods = ('db_flush', 'db_get', 'entry_add', 'entry_remove', 'entry_exists')

    def __del__(self):
        self.db_flush()


class JsonDB(DBCommunication):
    DB_PATH = os.path.join(os.path.dirname(__file__), "seen.json")

    def __init__(self, db_path=JsonDB.DB_PATH):
        self.db_path = db_path
        self.db = {}

    def db_flush(self):
        with open(self.db_path, "wb") as db_file:
            json.dump(self.db_get(), db_file)

    def db_get(self):
        if not self.db:
            with open(self.db_path, "rb") as db_file:
                try:
                    self.db = json.load(db_file)
                except Exception, e:
                    print "Warning:", e

        return self.db

    def entry_add(self, entry):
        self.db_get()[entry.index] = entry.to_json()

    def entry_remove(self, entry):
        if entry.index in self.db_get():
            del self.db[entry.index]
            return True
        return False

    def entry_exists(self, entry):
        return entry.index in self.db_get()
