from youtubesearchpython import (
    Suggestions,
    VideoSortOrder,
    VideosSearch,
)

class YouTubeScraper:
    """Abstract class for YouTube scraping."""

    def __init__(self, *args, **kwargs):
        """Abstract implementation of constructor."""

        raise NotImplementedError()

    def execute(self, *args, **kwargs):
        """Abstract implementation of execute method."""

        raise NotImplementedError()
    
    def rotate_proxy(self, *args, **kwargs):
        """Abstract implementation of proxy rotation method."""

        raise NotImplementedError()
    
    @staticmethod
    def get_popular_topics(amount: int) -> dict[str, str]:
        """Gets the most popular videos based on a topic.

        Args:
            amount (int): number of videos to retrieve

        Returns:
            dict[str, str]: dict containg retrieved data
        """
        query = VideosSearch(
            VideoSortOrder.viewCount,
            limit=amount, language='en', region='GB')
        return query.result()['result']

    @staticmethod
    def get_suggestions(topic: str) -> dict[str, str]:
        """Gets suggested videos for a given topic.

        Args:
            topic (str): topic to query

        Returns:
            dict[str, str]: dict containg retrieved data
        """
        suggestions = Suggestions(language='en', region='GB')
        topics = suggestions.get(topic)['result']
        del topics[0]
        return topics
    


    

    
    

    
