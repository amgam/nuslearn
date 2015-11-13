from dbase import DBase
from youtube import Youtube
import json

class Suggest:

    def __init__(self):
        self.db = DBase()
        self.yt = Youtube()


    def validateSuggestion(self, link, module_code, tags=""):
        #error codes
        #1 - wrong module code
        #2 - invalid link

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

        #how to check if tags are valid, stop_list perjaps
        response["is_valid"] = True
        response["err"] = "good"
        return json.dumps(response)
