from openai.error import RateLimitError
from openai.error import ServiceUnavailableError
from openai.error import InvalidRequestError
from .scrapers.metadata_scraper import MetaDataScraper
from .scrapers.transcript_scraper import TranscriptScraper
from .cleaners.metadata_cleaner import MetaDataCleaner
from .cleaners.transcript_cleaner import TranscriptCleaner
from .cleaners.data_cleaner import DataCleaner as dc
from ..gpt3 import summarize_yt_script_with_gpt3


class YouTubeScraperFactory:
    """Project specific factory class that abstracts library class methods
       for project specific YouTube scraping."""
    
    def __init__(self, metadata_scraper: object, transcript_scraper: object, amount: int):
        """Contructs YouTubeScraperFactory object.

        Args:
            metadata_scraper (object): MetaDataScraper object
            transcript_scraper (object): TranscriptScraper object
            amount (int): amount of videos required
        """

        self.metadata_scraper = metadata_scraper
        self.transcript_scraper = transcript_scraper
        self.metadata_cleaner = MetaDataCleaner()
        self.transcript_cleaner = TranscriptCleaner()
        self.amount = amount
        self.videos = set()
        self.result = []

    def execute(self) -> list[dict[str, any]]:
        """Returns 

        Returns:
            list[dict[str, any]]: full response for a scraping query
            in the format required for database insertions.
        """

        self._scrape()
        self.metadata_cleaner.full_clean(self.result)
        self.transcript_cleaner.full_clean(self.result)
        self._summarise_transcripts()
        self._remove_failed_summaries()
        return self.result

    def _scrape(self):
        """Scrapes YouTube and attempts to get retrieve unique metadata
           and transcripts, until the amount of data retrieved is
           equal to the required amount. Faulty responses are skipped.
        """

        response = self.metadata_scraper.execute()
        while len(self.result) < self.amount:
            metadata = next(response)
            video_id = metadata["video_id"]
            if video_id not in self.videos and dc.occupied_fields(metadata, 8):
                video_id = metadata["video_id"]
                transcript = self.transcript_scraper.execute(video_id)
                raw = transcript["transcript"]
                if not self._check_transcript_status(raw):
                    continue    
                metadata.update(transcript)
                self.result.append(metadata)
                self.videos.add(video_id)

    def _summarise_transcripts(self):
        """ Summarises all transcrips stored in self.response using
            ChatGPT API, failed summaries are discarded.
        """

        for data in self.result:
            try:
                transcript = data['transcript']
                data["summary"] = self.transcript_scraper.summarise(
                    transcript, summarize_yt_script_with_gpt3, 10)
            except (RateLimitError, ServiceUnavailableError,
                    InvalidRequestError):
                continue

    def _check_transcript_status(self, response: str) -> bool:
        """Checks if a recieved transcript is valid, and if not,
           handles any issues that occured.

        Args:
            response (str): raw transcript response

        Returns:
            bool: True if a valid transcript exists, False otherwise.
            Will rotate proxies if IP gets blocked.
        """

        if not response or response == "404":
            return False
        if response == "blocked":
            proxy = {"https" : "localhost"}
            self.metadata_scraper.rotate_proxy(proxy)
            self.transcript_scraper.rotate_proxy(proxy)
            return False
        return True
    
    def _remove_failed_summaries(self): 
        """Removes entries in self.result that do not have a valid
           summary, which could occur if the GPTAPI throws an error.
        """

        response = []
        for data in self.result:
            if "summary" in data:
                del data['transcript']
                response.append(data)
        self.result = response
        

def get_most_popular_video_transcripts_by_topic(topic: str, amount: int) -> list[dict[str, any]]:
    """Uses YouTubeScraperFactory class to generate metadata and summaries 
       for a number of YouTube videos for a given topic, abstracts the class
       for a cleaner API.

    Args:
        topic (str): topic to be queried
        amount (int): number of expected responses

    Returns:
        list[dict[str, any]]: query response in format suitable for
        database insertion.
    """

    params = ["keyword",
              "video_id",
              "channel_name",
              "video_name",
              "published_at",
              "views",
              "likes",
              "video_tags"]
    
    meta_scraper = MetaDataScraper(topic, params)
    transcript_scraper = TranscriptScraper()
    interface = YouTubeScraperFactory(meta_scraper, transcript_scraper, amount)
    return interface.execute()


        