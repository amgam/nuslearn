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

    def is_in_moduledb(self, term):
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
        print "tokens", tags, tokens
        self.processed_tokens = [self.stemmer.stem(word) for word in tokens if word not in self.stoplist]
        print "processed_tokens:", self.processed_tokens
        for word in self.processed_tokens:
            if self.is_in_moduledb(word) or self.is_in_tagdb(word):
                self.processed_tokens.remove(word)

        print "returning tokens:", self.processed_tokens
        return self.processed_tokens

    def validate_suggestion(self, link, module_code, tags):
        #error codes
        #1 - wrong module code
        #2 - invalid category, so reject suggestion
        self.db.connect()

        response = {}

        if module_code == "":
            mod_result = [1] #special case
        else:
            #validate module code first
            mod_result = self.db.retrieve("select * from ModuleTable where module_code=?", (module_code,))


        if not mod_result:
            print "MODULE CODE PROBLEM"
            response["is_valid"] = False
            response["err"] = "modprob"
            return (False, json.dumps(response))

        link_code = Youtube.extractID(link)

        if link_code == -1:
            print "LINK PROBLEM"
            response["is_valid"] = False
            response["err"] = "linkprob"
            return (False, json.dumps(response))

        #how to check if tags are valid, stop_list perhaps
        if self.make_tags_valid(tags):
            print "IZ GUT"
            response["is_valid"] = True
            response["err"] = "good"
            return (True, json.dumps(response))

        print "FAILS ALL??"
        print mod_result, link_code, self.make_tags_valid(tags)
        return (False, False)

    def insert_suggestion_to_db(self, link, module_code, tags):
        if self.validate_suggestion(link, module_code, tags):
            self.db.connect()
            if module_code:
                module_name = self.db.retrieve("select module_name from ModuleTable where module_code=?", (module_code,), True)["module_name"]
                module_prefix = filter(str.isalpha, str(module_code[:-1]))
                #YT retrieval
                vidInfo = self.yt.retrieveVideoInfo(link)
                self.db.insert("insert into GlobalVideoTable (module_code, module_name, module_prefix, vid_link, vid_title, vid_desc, votes) values (?, ?, ?, ?, ?, ?, ?)", (module_code, module_name, module_prefix, vidInfo["vid_id"], vidInfo["title"], vidInfo["description"], 0))
                for tag in self.processed_tokens:
                    self.db.insert("insert into GlobalTagTable (tags, vid_link, vid_title, vid_desc, votes) values (?, ?, ?, ?, ?)", (tag, vidInfo["vid_id"], vidInfo["title"], vidInfo["description"], 0))
            else:
                vidInfo = self.yt.retrieveVideoInfo(link)
                for tag in self.processed_tokens:
                    self.db.insert("insert into GlobalTagTable (tags, vid_link, vid_title, vid_desc, votes) values (?, ?, ?, ?, ?)", (tag, vidInfo["vid_id"], vidInfo["title"], vidInfo["description"], 0))

        self.db.save()
        self.db.close()
