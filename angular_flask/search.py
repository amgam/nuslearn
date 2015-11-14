from dbase import DBase
import json

class Search:
    def __init__(self):
        self.db = DBase()

    def look(self, userSearch):
        self.tokenize_search(userSearch)
        return self.get_results()

    def tokenize_search(self, userSearch):
        # example format would be "MA1521, calculus"
        self.searchTerms = userSearch.split(", ")

    def is_module_code(self, term):
        retrieveQuery = "select * from ModuleTable where module_code=?"
        result = self.db.retrieve(retrieveQuery, (term,), True)

        if result:
            return True
        else:
            return False

    def get_results(self):

        first_term = self.searchTerms[0]

        if len(self.searchTerms) == 1 and self.is_module_code(first_term):
            print "SEARCH TERM IS A MODULE CODE!!!!!"
        #this is a module
            retrieveQuery = "select * from GlobalVideoTable where module_code=?"

            results = self.db.retrieve(retrieveQuery, (first_term, ))

            serializable_info = map(lambda entry: {
                "module_code": entry["module_code"],
                "module_name": entry["module_name"],
                "module_prefix": entry["module_prefix"],
                "vid_link": entry["vid_link"],
                "vid_title": entry["vid_title"],
                "vid_desc": entry["vid_desc"],
                "votes": entry["votes"]
            }, results)

            output = {}
            output["searchTerm"] = serializable_info
            return json.dumps(output)

        elif (self.searchTerms == 1) and (self.is_module_code(first_term) == False):
            print "search term is a concept"
            retrieveQuery = "select * from GlobalTagTable where tags=?"
            results = self.db.retrieve(retrieveQuery, (first_term, ))
            serializable_info = map(lambda entry: {
                "tags": entry["tags"],
                "vid_link": entry["vid_link"],
                "votes": entry["votes"]
            }, results)

            output = {}
            output["searchTerm"] = serializable_info
            return json.dumps(output)

        elif len(self.searchTerms) > 1:
            temp_results = []
            output = {}
            output = []
            i=0;
            for term in self.searchTerms:
                temp_results[i] = []
                retrieveQuery = "select * from GlobalTagTable where tags=?"
                temp_results[i] = self.db.retrieve(retrieveQuery, (term, ))
                serializable_info = map(lambda entry: {
                    "tags": entry["tags"],
                    "vid_link": entry["vid_link"],
                    "votes": entry["votes"]
                }, temp_results[i])

                output = set(temp_results[0]).intersection(*temp_results)
            return json.dumps(output)
        else:
            print "Error: Unable to get results"
