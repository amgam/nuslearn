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
        if ", " in userSearch:
            self.searchTerms = userSearch.split(", ")
        elif "," in userSearch:
            self.searchTerms = userSearch.split(",")
        else:
            self.searchTerms = userSearch.split(" ")

    def is_module_code(self, term):
        retrieveQuery = "select * from ModuleTable where module_code=?"
        result = self.db.retrieve(retrieveQuery, (term.upper(),), True)

        if result:
            return True
        else:
            return False

    def get_results_by_module_code(self, code):
        retrieveQuery = "select * from GlobalVideoTable where module_code=?"

        results = self.db.retrieve(retrieveQuery, (module_code, ))

        serializable_info = map(lambda entry: {
            "module_code": entry["module_code"],
            "module_name": entry["module_name"],
            "module_prefix": entry["module_prefix"],
            "vid_link": entry["vid_link"],
            "vid_title": entry["vid_title"],
            "vid_desc": entry["vid_desc"],
            "votes": entry["votes"]
        }, results)

        return serializable_info

    def get_results_by_tag(self, term):
        retrieveQuery = "select * from GlobalTagTable where tags=?"
        results = self.db.retrieve(retrieveQuery, (concept, ))
        serializable_info = map(lambda entry: {
            "tags": entry["tags"],
            "vid_link": entry["vid_link"],
            "vid_title": entry["vid_title"],
            "vid_desc": entry["vid_desc"],
            "votes": entry["votes"]
        }, results)

        return serializable_info

    def get_results(self):

        print "Getting results..."

        first_term = self.searchTerms[0]
        size = len(self.searchTerms)

        if size == 1 and self.is_module_code(first_term):
            module_code = first_term.upper()
            module_name = self.db.retrieve("select * from ModuleTable where module_code=?", (module_code, ), True)["module_name"]
            identifier = module_code + " - " + module_name

            output = {}
            output[identifier] = self.get_results_by_module_code(module_code)
            return json.dumps(output)

        elif size == 1 and not self.is_module_code(first_term):
            concept = first_term.lower()

            output = {}
            identifier = "Concept: " + concept
            output[identifier] = self.get_results_by_tag(concept)
            return json.dumps(output)

        elif size > 1:
            temp_results = [[] for i in range(size)]
            output = []
            identifer = ""
            for i, term in enumerate(self.searchTerms):
                if self.if_module_code(term):
                    temp_results[i] = self.get_results_by_module_code(term.upper())
                else:
                    temp_results[i] = self.get_results_by_tag(term.lower())
                identifer = "Results: " + term
            combined = itertools.chain(temp_results)
            output_with_duplicates = list(combined)
            output_unique = set(output)
            output[identifier] = list(output_unique)
            return json.dumps(output)
        else:
            print "Error: Unable to get results"
