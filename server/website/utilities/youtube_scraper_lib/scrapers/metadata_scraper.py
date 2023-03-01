from .youtube_scraper import YouTubeScraper
from youtubesearchpython import (
    Video,
    VideoDurationFilter,
    CustomSearch,
)
import requests

class MetaDataScraper(YouTubeScraper):
    """Main class for YouTube metadata scraping."""

    def __init__(self, topic: str, params: list, proxy: dict[str, str]=None):
        """Constructs a MetaDataScraper object.

        Args:
            topic (str): topic to query on YouTube
            params (list): data of interest to extract, options are

                "video_id" -> the unquie id of a YouTube video
                "channel_name" -> name of the YouTube channel
                "video_name" -> name of the YouTube video
                "published_at" -> time of upload relative to current date
                "views" -> number of views at the current date
                "likes" -> number of likes at the curretn date
                "video_tags" -> associated keywords for the video

            proxy (dict[str, str], optional): proxies for scraping
        """
        self.topic = topic
        self.params = params
        self.proxy = proxy

    @staticmethod
    def get_likes(url: str) -> str:
        """Retrieves number of likes for a video.

        Args:
            url (str): full url of video

        Returns:
            str: number of likes for the video, may be raw hmtl
        """

        try:
            response = requests.get(url, headers={'User-Agent': ''}, timeout=50)
            likes = response.text[:response.text.find(' likes"')]
            return likes[likes.rfind('"') + 1:]
        except TimeoutError:
            return ""

    @staticmethod
    def get_views(url: str) -> str:
        """Retrieves number of views for a video.

        Args:
            url (str): full url of video

        Returns:
            str: number of views for the video, may be raw hmtl
        """

        try:
            response = requests.get(url, headers={'User-Agent': ''}, timeout=50)
            views = response.text[:response.text.find(' views"')]
            return views[views.rfind('"') + 1:]
        except TimeoutError:
            return ""
    
    @staticmethod
    def get_keywords(url: str) -> list[str]:
        """Retrieves all associated tags for a video.

        Args:
            url (str): full url of video

        Returns:
            list[str]: list of video tags, or None if failed
        """

        try:
            return Video.get(url)["keywords"]
        except (TypeError, ValueError):
            return None
        
    def rotate_proxy(self, proxy: dict[str, str]):
        """Rotates current proxy in case of IP block.

        Args:
            proxy (dict[str, str]): new proxy
        """

        self.proxy = proxy

    def execute(self, language: str='en', region: str='GB', limit: int=20):
        """Executes a live search for the given topic.

        Args:
            language (str, optional): language of video, default is 'en'
            region (str, optional): country, default is 'GB'
            limit (int, optional): number of videos per page, default is 20

        Yields:
            Generator[dict[str, str]]: current metadata scraped from a page
        """

        query = CustomSearch(self.topic, VideoDurationFilter.short,
                language=language, region=region, limit=limit)
        while True:
            result = query.result()['result']
            for response in result:
                yield self._process_query(response)
            query.next()

    def _process_query(self, result: dict[str, str]) -> dict[str, str]:
        """Helper method to extract relevant metadata.

        Args:
            result (dict[str, str]): raw metadata

        Returns:
            dict[str, str]: filtered metadata, with only self.params
        """

        metadata, final = self._get_metadata(result), dict()
        for key, value in metadata.items():
            if key in self.params:
                final[key] = value
        return final


    def _get_metadata(self, result: dict[str, str]) -> dict[str, str]:
        """Helper method to extract metadata from raw query response

        Args:
            result (dict[str, str]): raw query response

        Returns:
            dict[str, str]: all relevant metadata
        """
        
        metadata = {"keyword" : self.topic,
                "video_id" : result['id'],
                "channel_name" : result['channel']['name'],
                "video_name" : result['title'],
                "published_at" : result['publishedTime'],
                "views" : self.get_views(result['link']),
                "likes" : self.get_likes(result['link']),
                "video_tags" : self.get_keywords(result['link'])
                }
        return metadata
