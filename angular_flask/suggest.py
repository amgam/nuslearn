from dbase import DBase
from youtube import Youtube
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import json

class Suggest:

    def __init__(self):
        self.db = DBase()
        self.yt = Youtube()
        self.stemmer = PorterStemmer()
        self.stoplist = stopwords.words('english')
        self.processed_tokens = []

    def tokenize(self, tags):
        if ", " in tags:
            return tags.split(", ")
        elif "," in tags:
            return tags.split(",")
        else:
            return tags.split()

    def is_module_code(self, term):
        self.db.connect()
        retrieveQuery = "select * from ModuleTable where module_code=?"
        result = self.db.retrieve(retrieveQuery, (term.upper(),), True)

        self.db.close()
        if result:
            return True
        else:
            return False

    def is_in_tagdb(self, tag):
        self.db.connect()
        retrieveQuery = "select * from GlobalTagTable where tags=?"
        result = self.db.retrieve(retrieveQuery, (tag.lower(),), True)

        self.db.close()
        if result:
            return True
        else:
            return False

    def make_tags_valid(self, tags):
        tokens = self.tokenize(tags)
        self.processed_tokens = [stemmer.stem(word) for word in tokens if word not in stoplist]
        for word in self.processed_tokens:
            if word is_module_code() or word is_in_tagdb():
                self.processed_tokens.remove(word)

        return self.processed_tokens

    def validate_suggestion(self, link, module_code, tags):
        #error codes
        #1 - wrong module code
        #2 - invalid category, so reject suggestion

        response = {}

        #validate module code first
        mod_result = self.db.retrieve("select * from ModuleTable where module_code=?", (module_code,))

        if not mod_result:
            response["is_valid"] = False
            response["err"] = "modprob"
            return json.dumps(response)

            link_code = Youtube.extractID(link)

            if link_code == -1:
                response["is_valid"] = False
                response["err"] = "linkprob"
                return json.dumps(response)

            #how to check if tags are valid, stop_list perhaps
            if self.make_tags_valid(tags):
                response["is_valid"] = True
                response["err"] = "good"
                return json.dumps(response)

        return False

    def insert_suggestion_to_db(self, link, module_code, tags):
        self.db.connect()
        if self.validate_suggestion(link, module_code, tags):
            module_name = self.retrieve("select module_name from ModuleTable where module_code=?", (module_code,), True)["module_name"]
            module_prefix = filter(str.isalpha, module_code[:-1])
            #YT retrieval
            vidInfo = self.yt.retrieveVideoInfo(videolink)
            self.insert("insert into GlobalVideoTable (module_code, module_name, module_prefix, vid_link, vid_title, vid_desc, votes) values (?, ?, ?, ?, ?, ?, ?)", (module_code, module_name, module_prefix, vidInfo["vid_id"], vidInfo["title"], vidInfo["description"], 0))
            for tag in self.processed_tokens:
                self.insert("insert into GlobalTagTable (tags, vid_link, vid_title, vid_desc, votes) values (?, ?, ?, ?, ?)", (tag, vidInfo["vid_id"], vidInfo["title"], vidInfo["description"], 0))
        self.db.close()
