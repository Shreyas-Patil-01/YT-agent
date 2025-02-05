import os
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()

class YouTubeSearch:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.api_key)

    def search_videos(self, query, max_results=1):
        request = self.youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        return response.get("items", [])