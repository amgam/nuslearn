from dbase import DBase
import json
import itertools

class Search:
    def __init__(self):
        self.db = DBase()

    def look(self, userSearch, matric):
        self.matric = matric
        self.tokenize_search(userSearch)
        return self.get_results()

    def tokenize_search(self, userSearch):
        self.originalMultiSearch = userSearch

        if ", " in userSearch:
            self.searchTerms = userSearch.split(", ")
        elif "," in userSearch:
            self.searchTerms = userSearch.split(",")
        else:
            self.searchTerms = userSearch.split(" ")

    def is_module_code(self, term):
        self.db.connect()
        retrieveQuery = "select * from ModuleTable where module_code=?"
        result = self.db.retrieve(retrieveQuery, (term.upper(),), True)

        self.db.close()
        if result:
            return True
        else:
            return False

    def get_results_by_module_code(self, module_code):
        retrieveQuery = "select * from GlobalVideoTable where module_code=? order by votes desc"
        self.db.connect()
        results = self.db.retrieve(retrieveQuery, (module_code, ))

        serializable_info = map(lambda entry: {
            "module_code": entry["module_code"],
            "module_name": entry["module_name"],
            "module_prefix": entry["module_prefix"],
            "vid_link": entry["vid_link"],
            "vid_title": entry["vid_title"],
            "vid_desc": entry["vid_desc"],
            "votes": entry["votes"],
            "hasVoted": self.db.retrieve("select * from VotedVideosTable where (vid_link=?) and (matric=?)", (entry["vid_link"], self.matric), True)
        }, results)

        for item in serializable_info:
            if item["hasVoted"]:
                item["hasVoted"] = item["hasVoted"]["hasVoted"] # access row
            else:
                item["hasVoted"] = 0;

        self.db.close()
        return serializable_info

    def get_results_by_tag(self, term):
        retrieveQuery = "select * from GlobalTagTable where tags=? order by votes desc"
        self.db.connect()

        results = self.db.retrieve(retrieveQuery, (term, ))
        serializable_info = map(lambda entry: {
            "tags": entry["tags"],
            "vid_link": entry["vid_link"],
            "vid_title": entry["vid_title"],
            "vid_desc": entry["vid_desc"],
            "votes": entry["votes"],
            "hasVoted": self.db.retrieve("select * from VotedVideosTable where (vid_link=?) and (matric=?)", (entry["vid_link"], self.matric), True)
        }, results)

        for item in serializable_info:
            if item["hasVoted"]:
                item["hasVoted"] = item["hasVoted"]["hasVoted"] # access row
            else:
                item["hasVoted"] = 0;

        self.db.close()
        return serializable_info

    def get_results(self):

        print "Getting results..."

        first_term = self.searchTerms[0]
        size = len(self.searchTerms)

        toReturn = ""

        if size == 1 and self.is_module_code(first_term):
            self.db.connect()
            print "size 1, is module"
            module_code = first_term.upper()
            module_name = self.db.retrieve("select * from ModuleTable where module_code=?", (module_code, ), True)["module_name"]
            identifier = module_code + " - " + module_name

            output = {}
            output[identifier] = self.get_results_by_module_code(module_code)
            toReturn = json.dumps(output)

        elif size == 1 and not self.is_module_code(first_term):
            self.db.connect()

            print "size 1, is concept"
            concept = first_term.lower()

            output = {}
            identifier = "Concept: " + concept
            output[identifier] = self.get_results_by_tag(concept)
            toReturn = json.dumps(output)

        elif size > 1:
            self.db.connect()

            print "multiple"
            temp_results = []
            output = {}
            identifier = ""
            for term in self.searchTerms:
                if self.is_module_code(term):
                    temp_results += self.get_results_by_module_code(term.upper())
                else:
                    temp_results += self.get_results_by_tag(term.lower())
            identifier = "Concepts: " + self.originalMultiSearch
            print temp_results
            output_unique = {v['vid_link']:v for v in temp_results}.values()
            output[identifier] = output_unique
            toReturn = json.dumps(output)
        else:
            print "Error: Unable to get results"

        # self.db.close()
        return toReturn
