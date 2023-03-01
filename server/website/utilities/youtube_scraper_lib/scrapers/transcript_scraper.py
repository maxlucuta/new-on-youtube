from youtube_transcript_api import YouTubeTranscriptApi
from .youtube_scraper import YouTubeScraper
import youtube_transcript_api, time


class TranscriptScraper(YouTubeScraper):
    """Main class for scraping YouTube transcripts."""
    
    def __init__(self, proxy: dict=None):
        """Constructs a YouTubeTranscriptScraper object.

        Args:
            proxy (dict, optional): dict of proxy in format
            {http/https : IP}, default is None
        """

        self.proxy = proxy
    
    def rotate_proxy(self, proxy: dict):
        """Changes current proxy for scraping in the case
           YouTube has blocked the current IP.

        Args:
            proxy (dict): dict of proxy in the format
            {http/https : IP}.
        """

        self.proxy = proxy

    def execute(self, video_id: str) -> dict[str, str]:
        """Fetches summaries for a given Video ID.

        Args:
            video_id (str): YouTube video ID.

        Returns:
            dict[str, str]: a dict in the format
            {transcript : response}, where the response is
            either a raw transcript, or an error code.
        """
    
        response = {"transcript" : None}
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=['en', 'en-GB'], proxies=self.proxy)
            response["transcript"] = transcript
        except (youtube_transcript_api.NoTranscriptFound,
                youtube_transcript_api.TranscriptsDisabled,
                youtube_transcript_api.NoTranscriptAvailable):
            response["transcript"] = "404"
        except youtube_transcript_api.YouTubeRequestFailed:
            response["transcript"] = "blocked"
        return response
    
    def insert(self, transcript: dict[str, str], data: dict):
        """Inserts transcript data into an existing dict.

        Args:
            transcript (dict[str, str]): dict containing transcript
            data (dict): dict containing existing data
        """

        data.update(transcript)

    @staticmethod
    def summarise(transcript: str, summariser: callable, limiter: int=0) -> str:
        """Generates a summary of a YouTube transcript using a given callable
           summarisation method and returns it.

        Args:
            transcript (str): YouTube transcript
            summariser (callable): Callable summariser method
            limiter (int): optional rate limiter, default is 0

        Returns:
            str: summarised transcript
        """

        task = "Please summarise this transcript for me in a \
        few sentences: " + transcript + "\n\nTl;dr"
        summary = summariser(task)
        summary = summary.strip(" :-")
        time.sleep(limiter)
        return summary

