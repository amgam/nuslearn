import os
import sqlite3

class DBase:
    def __init__(self):
        self.file_path = "/angular_flask/static/"
        self.db_name = "nuslearn.db"
        self.db_path = os.getcwd() + self.file_path + self.db_name
        self.db_is_new = not os.path.exists(self.db_path)

        self.connect()

        if self.db_is_new:
            self.init_schema()


    def init_schema(self):
        self.schema_filename = "schema.sql"
        self.schema_path = os.getcwd() + self.file_path + self.schema_filename

        with open(self.schema_path, 'rt') as f:
                self.schema = f.read()

        self.conn.executescript(self.schema)


    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def insert(self, statement):
        self.conn.execute(statement)

    def retrieve(self, statement):
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def save(self):
        print "saved!"
        self.conn.commit()

        # for row in self.cursor.fetchall():
        #     print row
