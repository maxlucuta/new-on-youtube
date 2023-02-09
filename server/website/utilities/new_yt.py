from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery as googleapi
from .gpt3 import summarize_yt_script_with_gpt3
from openai.error import RateLimitError, ServiceUnavailableError
from youtubesearchpython import *
import youtube_transcript_api, time, functools, requests, openai

class YoutubeParser:

    def __init__(self, topic, amount):
        self.topic = topic
        self.amount = amount
        self.videos = set()
        self.response = []

    
    def execute(self, rate=1):
        self._search()
        self._generate_summaries(rate)
        self.response = self._garbage_collector()
        return self.response

    
    def exception_handler(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try: func(*args, **kwargs)
            except TypeError: pass
            except KeyError: pass
        return wrapper
    

    def _search(self):
        query = CustomSearch(self.topic, VideoDurationFilter.short,
        language='en', region='US', limit=self.amount)
        while len(self.response) < self.amount:
            result = query.result()['result']
            for i in range(len(result)):
                if len(self.response) >= self.amount: break
                self._insert_results(result[i])
            query.next()
        return 


    @exception_handler
    def _insert_results(self, result):
        if result['id'] in self.videos: return
        data = dict()
        data["keyword"] = self.topic
        data["video_id"] = result['id']
        data["video_name"] = result['title']
        data["channel_name"] = result['channel']['name'] 
        data['views'] = result['viewCount']['text']
        data['published_at'] = result['publishedTime']
        data['likes'] = self._get_likes(result['link'])
        data["video_tags"] = self.get_keywords(result['link'])
        if not self._has_transcript_available(data): return
        if not self._no_empty_fields(data): return 
        self._convert_ints(data)
        self.response.append(data)
        self.videos.add(result['id'])
        return


    def _no_empty_fields(self, data):
        for i in data:
            if not data[i]:
                return False
        return len(data) == 9


    def _has_transcript_available(self, data):
        try:
            raw = YouTubeTranscriptApi.get_transcript(
            data['video_id'], languages=['en', 'en-GB'])
            transcript = self._format_transcript(raw)
            data['transcript'] = transcript
        except (youtube_transcript_api.NoTranscriptFound,
            youtube_transcript_api.TranscriptsDisabled,
            youtube_transcript_api.NoTranscriptAvailable,
            youtube_transcript_api.YouTubeRequestFailed):
            return False
        return True
         

    def _convert_ints(self, data):
        likes = "".join([i for i in data['likes'] if i.isdigit()])
        views = "".join([i for i in data['views'] if i.isdigit()])
        data['likes'] = int(likes) if likes else 0
        data['views'] = int(views) if views else 0
        return

    
    def _get_likes(self, url):
        r = requests.get(url, headers={'User-Agent': ''})
        likes = r.text[:r.text.find(' likes"')]
        dislikes = r.text[:r.text.find(' dislikes"')]
        return likes[likes.rfind('"') + 1:]


    def _format_transcript(self, raw_transcript):
        final_transcript = []
        for text in raw_transcript:
            word = text.get('text')
            if not word or word == '[Music]':
                continue
            final_transcript.append(word)
        return " ".join(final_transcript)


    def _generate_summaries(self, rate):
        count = 0
        for data in self.response:
            try:
                transcript = data['transcript']
                data["summary"] = self.summarise(transcript, rate)
                count += 1
                print("Got " + str(count) + " video(s)!")
            except (RateLimitError, ServiceUnavailableError): 
                continue
        return 

    
    def _garbage_collector(self):
        new_response = []
        for data in self.response:
            if "summary" in data:
                del data['transcript']
                new_response.append(data)
        return new_response


    @staticmethod
    def get_keywords(url):
        return Video.get(url)["keywords"]


    @staticmethod
    def get_suggestions(topic):
        suggestions = Suggestions(language='en', region='US')
        topics = suggestions.get(topic)['result']
        del topics[0]
        return topics


    @staticmethod
    def summarise(transcript, limiter, keywords=None):
        task = "Please summarise this transcript for me in a \
        few sentences: " + transcript + "\n\nTl;dr"
        summary = summarize_yt_script_with_gpt3(task)
        summary = summary.strip(" :-")
        time.sleep(limiter)
        return summary


    @staticmethod
    def get_popular_topics(amount):
        query = VideoSearch(VideoSortOrder.viewCount, 
        limit = amount, language = 'en', region = 'US')
        return query.result()['result']


def get_most_popular_video_transcripts_by_topic(topic, amount, rate=10):
    parser = YoutubeParser(topic, amount)
    return parser.execute(rate)


        











