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

        # else:
