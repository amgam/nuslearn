import requests

class Youtube:
    def __init__(self):
        self.api_key = "AIzaSyB3oRVZ1Lahd5j2JqG0zWrA9g-75GfUYkU"

    def retrieveVideoInfo(self, videoLink):
        # ?id=itemId&key=apiKey&fields=items(snippet(title))&part=snippet
        request_url = "https://www.googleapis.com/youtube/v3/videos"
        # auth_details = {'id': "0FECUG7k5gY", 'key': self.api_key, 'fields': "items(snippet(title))&part=snippet"}
        auth_details = {'part': "snippet", 'id': "SLvTCHhu5SE", 'key': self.api_key}

        # GET https://www.googleapis.com/youtube/v3/videos?part=snippet&id=rmfmdKOLzVI&key={YOUR_API_KEY}

        resp = requests.get(request_url, params=auth_details)
        return (resp.text, resp.status_code, resp.headers.items())

    # def validation(self, videolink):
