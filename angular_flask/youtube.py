import requests

class Youtube:
    def __init__(self):
        self.api_key = "AIzaSyB3oRVZ1Lahd5j2JqG0zWrA9g-75GfUYkU"

    @staticmethod
    def extractID(URL):
        #https://www.youtube.com/watch?v=5u8rFbpdvds single video
        #https://www.youtube.com/watch?v=bX3jvD7XFPs&list=PLB2BE3D6CA77BB8F7 playlist
        # ID is always 11 chars
        error = -1

        if Youtube.validateURL(URL):
            startIndex = URL.find("?v=")

            if startIndex == -1:
                return error

            return URL[startIndex + 3 : startIndex + 14]
        else:
            return error

    @staticmethod
    def validateURL(URL):
        return False if "https://www.youtube.com/watch?v=" not in URL else True

    @staticmethod
    def validateCategory(categoryId):
        howto_style = "26"
        education = "27"

        return True if categoryId == howto_style or categoryId == education else False

    def retrieveVideoInfo(self, videoLink, charLimit=300):
        # ?id=itemId&key=apiKey&fields=items(snippet(title))&part=snippet
        request_url = "https://www.googleapis.com/youtube/v3/videos"
        # auth_details = {'id': "0FECUG7k5gY", 'key': self.api_key, 'fields': "items(snippet(title))&part=snippet"}
        ytLink = Youtube.extractID(videoLink)
        if ytLink == -1:
            return False  #invalid link


        auth_details = {'part': "snippet", 'id': ytLink, 'key': self.api_key}

        # GET https://www.googleapis.com/youtube/v3/videos?part=snippet&id=rmfmdKOLzVI&key={YOUR_API_KEY}

        resp = requests.get(request_url, params=auth_details)
        jsonResponse = resp.json()

        snips = jsonResponse["items"][0]["snippet"]

        title = snips["title"]
        categoryId = snips["categoryId"]
        description = snips["description"]

        if len(description) > charLimit:
            description = description[:charLimit] + "..."

        return {"title": title, "description": description, "vid_id": ytLink, "categoryId": categoryId}
