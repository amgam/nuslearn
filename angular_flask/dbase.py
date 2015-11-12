import os
import sqlite3
import json

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
        print "Initializing Database"
        self.schema_filename = "schema.sql"
        self.schema_path = os.getcwd() + self.file_path + self.schema_filename

        with open(self.schema_path, 'rt') as f:
                self.schema = f.read()

        self.conn.executescript(self.schema)

        #schema now exists

        #read in module listings
        jsonPath = os.getcwd() + self.file_path + "moduleList.json"
        with open(jsonPath) as json_file:
            modules = json.load(json_file)

        #populate db
        parsed_modules = map(lambda x: (x["ModuleCode"], x["ModuleTitle"]), modules) #parses into tuple format
        self.conn.executemany('insert into ModuleTable values (?,?)', parsed_modules)


    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def insert(self, statement, variables=False):
        if variables:
            self.conn.execute(statement, variables)
        else:
            self.conn.execute(statement)

    def retrieve(self, statement, variables=False):
        if variables:
            return self.conn.execute(statement, variables)
        else:
            return self.conn.execute(statement)
            
    def save(self):
        print "\nsaved!"
        self.conn.commit()

        # for row in self.cursor.fetchall():
        #     print row

    # Populate GlobalVideoTable
    def populateGlobalVideoTable(self):
        filepath = 'angular_flask/static/training_data/training.txt'
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    videolinks = line.split()
                    module_code = videolinks[0]
                    for videolink in videolinks[1:]:
                        module_name = self.retrieve("select * from ModuleTable where module_code=?", module_code)
                        module_prefix = filter(str.isalpha, module_code[:-1])
                        self.insert("insert into GlobalVideoTable (module_code, module_name, module_prefix, vid_link) values (?, ?, ?, ?)", (module_code, module_name, module_prefix, videolink))
            print "GlobalVideoTable is populated with data"
        except IOError:
            print "Error: File not found or unreadable file"
