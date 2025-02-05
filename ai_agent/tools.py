from youtube_api.search import YouTubeSearch

class YouTubeSearchTool:
    def __init__(self):
        self.youtube_search = YouTubeSearch()

    def search(self, query):
        """Search YouTube for videos based on a query."""
        results = self.youtube_search.search_videos(query)
        return results