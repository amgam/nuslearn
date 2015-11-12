import requests
import json

class Learner:


    def __init__(self, token):
        self.token = token;
        self.api_key = "yWIyIVdgoDbQz9EUdJ06x"
        self.retrieve_username()
        self.retrieve_matric()
        self.retrieve_modules()

    def get_token(self):
        return self.token

    # def retrieve_profile(self):
    #
    #     ivle_url = "https://ivle.nus.edu.sg/api/Lapi.svc/Profile_View"
    #     auth_details = {'APIKey': self.api_key, 'AuthToken': self.token}
    #
    #     r = requests.get(ivle_url, params=auth_details)
    #     self.profile = (r.text, r.status_code, r.headers.items())

    def retrieve_username(self):
        #retrieve username from IVLE
        ivle_url = "https://ivle.nus.edu.sg/api/Lapi.svc/UserName_Get"
        auth_details = {'APIKey': self.api_key, 'Token': self.token}

        r = requests.get(ivle_url, params=auth_details)
        self.username = r.text

    def retrieve_matric(self):
        #retrieve username from IVLE
        # https://ivle.nus.edu.sg/api/Lapi.svc/UserID_Get?APIKey={System.String}&Token={System.String}
        ivle_url = "https://ivle.nus.edu.sg/api/Lapi.svc/UserID_Get"
        auth_details = {'APIKey': self.api_key, 'Token': self.token}

        r = requests.get(ivle_url, params=auth_details)
        self.matric = r.text
        # print "token", self.token, type(self.token)
        # print "matric no:", self.matric, type(self.matric)

    def retrieve_modules(self):
        #retrieve modules from IVLE
        # https://ivle.nus.edu.sg/api/Lapi.svc/Modules_Taken?APIKey={System.String}&AuthToken={System.String}&StudentID={System.String}
        # https://ivle.nus.edu.sg/api/Lapi.svc/Modules?APIKey={System.String}&AuthToken={System.String}&Duration={System.Int32}&IncludeAllInfo={System.Boolean}
        # https://ivle.nus.edu.sg/api/Lapi.svc/Timetable_Student?APIKey={System.String}&AuthToken={System.String}&AcadYear={System.String}&Semester={System.String}
        # https://ivle.nus.edu.sg/api/Lapi.svc/Modules_Student?APIKey={System.String}&AuthToken={System.String}&Duration={System.Int32}&IncludeAllInfo={System.Boolean}
        # ivle_url = "https://ivle.nus.edu.sg/api/Lapi.svc/Modules_Taken"
        ivle_url = "https://ivle.nus.edu.sg/api/Lapi.svc/Modules_Student"



        # auth_details = {'APIKey': self.api_key, 'AuthToken': self.token, 'AcadYear': "2015/2016", 'Semester': "1"}
        # print "orig mat", self.matric, type(self.matric)
        # print "str", str(self.matric), type(str(self.matric))
        # print "typed", type("a0119264")
        # print "IM here", self.matric
        auth_details = {'APIKey': self.api_key, 'AuthToken': self.token, 'Duration': 1, 'IncludeAllInfo': False}

        resp = requests.get(ivle_url, params=auth_details)

        output = {}

        for mod in resp.json()["Results"]:
            output[mod["CourseCode"]] = mod["CourseName"]

        # mods = map(lambda x: {"CourseCode": x["CourseCode"], "CourseName": x["CourseName"]} , resp.json()["Results"])
        self.modules = output
        # print

    def get_username(self):
        return self.username

    def get_matric(self):
        return self.matric

    def get_modules(self):
        return json.dumps(self.modules)
