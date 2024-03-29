import os
import sqlite3
import json
from youtube import Youtube

class DBase:
    def __init__(self):
        self.file_path = "/angular_flask/static/"
        self.db_name = "nuslearn.db"
        self.db_path = os.getcwd() + self.file_path + self.db_name
        self.db_is_new = not os.path.exists(self.db_path)
        self.yt = Youtube()
        self.connect()

        if self.db_is_new:
            self.init_schema()
            self.populateGlobalVideoTable()
            self.populateGlobalTagTable()

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
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def insert(self, statement, variables):
        if variables:
            self.cursor.execute(statement, variables)
        else:
            self.cursor.execute(statement)

    def update(self, statement, variables):
        if variables:
            self.cursor.execute(statement, variables)
        else:
            self.cursor.execute(statement)

    def retrieve(self, statement, variables=False, isSingluar=False):
        if variables:
            self.cursor.execute(statement, variables)
        else:
            self.cursor.execute(statement)

        if isSingluar:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def save(self):
        print "\nsaved!"
        self.conn.commit()

    def close(self):
        self.conn.close()

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
                        module_name = self.retrieve("select module_name from ModuleTable where module_code=?", (module_code,), True)["module_name"]
                        module_prefix = filter(str.isalpha, module_code[:-1])

                        #YT retrieval
                        vidInfo = self.yt.retrieveVideoInfo(videolink)

                        #vid_link needs to be manipulated for it to be displayed on site.
                        embed_link = videolink.replace("watch?v=", "embed/")
                        self.insert("insert into GlobalVideoTable (module_code, module_name, module_prefix, vid_link, vid_title, vid_desc, votes) values (?, ?, ?, ?, ?, ?, ?)", (module_code, module_name, module_prefix, vidInfo["vid_id"], vidInfo["title"], vidInfo["description"], 0))
            print "GlobalVideoTable is populated with data"
            self.save()
        except IOError:
            print "Error: File not found or unreadable file"

    # Populate GlobalTagTable for testing purposes
    def populateGlobalTagTable(self):
        filepath = 'angular_flask/static/training_data/training_tags.txt'
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    tokens = line.split()
                    tag = tokens[0]
                    for token in tokens[1:]:
                        vid_link = token;

                        #YT retrieval
                        vidInfo = self.yt.retrieveVideoInfo(token)

                        self.insert("insert into GlobalTagTable (tags, vid_link, vid_title, vid_desc, votes) values (?, ?, ?, ?, ?)", (tag, vidInfo["vid_id"], vidInfo["title"], vidInfo["description"], 0))
            self.save()
            print "GlobalTagTable is populated with tags (socket, programming, java, network) for CS2105"
        except IOError:
            print "Error: File not found or unreadable file"
