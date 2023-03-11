from .youtube_scraper import YouTubeScraper
from youtubesearchpython import (
    Video,
    CustomSearch,
)
import requests


class MetaDataScraper(YouTubeScraper):
    """Main class for YouTube metadata scraping."""

    def __init__(self, topic: str, params: list, proxy: dict[str, str] = None):
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
                "duration" -> length of the video
                "visible" -> public or private video

            proxy (dict[str, str], optional): proxies for scraping
        """
        self.topic = topic
        self.params = params
        self.proxy = proxy

    @staticmethod
    def get_likes(url: str, proxy: dict[str, str] = None) -> str:
        """Retrieves number of likes for a video.

        Args:
            url (str): full url of video
            proxy dict[str, str]: http proxy in requests format

        Returns:
            str: number of likes for the video, may be raw hmtl
        """

        try:
            response = requests.get(
                url, headers={'User-Agent': ''}, timeout=50, proxies=proxy)
            likes = response.text[:response.text.find(' likes"')]
            return likes[likes.rfind('"') + 1:]
        except Exception:
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
            videoInfo = Video.getInfo(url)
            return videoInfo['viewCount']['text']
        except (TypeError, ValueError):
            return None

    @staticmethod
    def get_upload_date(url: str) -> str:
        """Retrieves the upload date for a video.

        Args:
            url (str): full url of video

        Returns:
            str: upload date in format yy:mm:dd
        """

        try:
            metadata = Video.get(url, get_upload_date=True)
            return metadata.get("publishDate")
        except (TypeError, ValueError):
            return None

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

    def execute(self, language: str = 'en', region: str = 'GB',
                limit: int = 20):
        """Executes a live search for the given topic.

        Args:
            language (str, optional): language of video, default is 'en'
            region (str, optional): country, default is 'GB'
            limit (int, optional): number of videos per page, default is 20

        Yields:
            Generator[dict[str, str]]: current metadata scraped from a page
        """

        query = CustomSearch(self.topic, "EgQQARgD",
                             language=language, region=region, limit=limit)
        while True:
            result = query.result()['result']
            for response in result:
                yield self._process_query(response)
            try:
                if not query.next():
                    break
            except Exception:
                print("IP has been blocked!", flush=True)
                break

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

        metadata = {"keyword": self.topic,
                    "video_id": result['id'],
                    "channel_name": result['channel']['name'],
                    "video_name": result['title'],
                    "published_at": result['publishedTime'],
                    "views": result['viewCount']['text'],
                    "likes": self.get_likes(result['link'], self.proxy),
                    "video_tags": self.get_keywords(result['link']),
                    "duration": result['duration'],
                    "visible": self._video_is_public(result['link'],
                                                     self.proxy)
                    }

        return metadata

    @staticmethod
    def _video_is_public(url: str, proxies: dict = None) -> bool:
        """Checks if a video is public or private.

        Args:
            url (str): url of the video

        Returns:
            bool: True if the video is public, false if
            it is private
        """

        try:
            response = requests.get(url, timeout=50, proxies=proxies)
            if "Private video" in response.text:
                return False
            return True
        except Exception:
            return False
