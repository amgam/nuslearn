import requests

class Youtube:
    def __init__(self):
        self.api_key = "AIzaSyCzYaUgUG6SlJbAo6-gByfwEPwEuTTvgZ0"

    def retrieveVideoInfo(self, videoLink):
        # ?id=itemId&key=apiKey&fields=items(snippet(title))&part=snippet
        request_url = "https://www.googleapis.com/youtube/v3/videos"
        auth_details = {'id': "0FECUG7k5gY", 'key': self.api_key, 'fields': "items(snippet(title))&part=snippet"}

        resp = requests.get(request_url, params=auth_details)
        return (resp.text, resp.status_code, resp.headers.items())

    # def validation(self, videolink):
