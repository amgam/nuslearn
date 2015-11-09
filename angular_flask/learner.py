import requests

class Learner:

    def __init__(self, token):
        self.token = token;
        self.api_key = "yWIyIVdgoDbQz9EUdJ06x"
        self.retrieve_username()

    def get_token(self):
        return self.token

    def retrieve_username(self):
        #retrieve username from IVLE
        ivle_url = "https://ivle.nus.edu.sg/api/Lapi.svc/UserName_Get"
        auth_details = {'APIKey': self.api_key, 'Token': self.token}

        r = requests.get(ivle_url, params=auth_details)
        self.username = r.text

    def get_username(self):
        return self.username
