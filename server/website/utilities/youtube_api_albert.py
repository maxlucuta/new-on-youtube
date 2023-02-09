# from youtube_transcript_api import YouTubeTranscriptApi
# import googleapiclient.discovery as googleapi
# from .gpt3 import summarize_yt_script_with_gpt3
# from youtubesearchpython import *
# import youtube_transcript_api, time, pafy


# class YoutubeParser:

#     def __init__(self, topic, amount):
#         self.topic = topic
#         self.amount = amount
#         self.response = []

    
#     def execute(self, rate=1):
#         self._search()
#         self._generate_summaries(rate)
#         return self.response


#     def _search(self):
#         query = CustomSearch(self.topic, VideoSortOrder.viewCount, 
#         limit = self.amount, language = 'en', region = 'US')
#         result = query.result()['result']
#         [self._insert_results(result[i]) for i in range(self.amount)]
#         return


#     def _insert_results(self, result, data={}):
#         data["keyword"] = self.topic
#         data["url"] = result['link']
#         data["video_id"] = result['id']
#         data["video_name"] = result['title']
#         data["channel_name"] = result['channel']['name'] 
#         data['views'] = result['viewCount']['text']
#         data['published_at'] = result['publishedTime']
#         data['likes'] = pafy.new(data['url']).likes
#         data["video_tags"] = self._get_keywords(data["url"])
#         del data["url"]
#         self.response.append(data)
#         return


#     def _format_transcript(self, raw_transcript):
#         final_transcript = []
#         for text in raw_transcript:
#             word = text.get('text')
#             if not word or word == '[Music]':
#                 continue
#             final_transcript.append(word)
#         return " ".join(final_transcript)


#     def _generate_summaries(self, rate):
#         for i in range(len(self.response[:])):
#             data = self.response[i]
#             try:
#                 id = data.get('video_id')
#                 raw = YouTubeTranscriptApi.get_transcript(
#                 id, languages=['en', 'en-GB'])
#                 transcript = self._format_transcript(raw)
#                 data["summary"] = self._summarise(transcript, rate)
#             except youtube_transcript_api.NoTranscriptFound:
#                 del self.response[i]


#     @staticmethod
#     def _get_keywords(url):
#         return Video.get(url)["keywords"]


#     @staticmethod
#     def _summarise(transcript, limiter, keywords=None):
#         task = "Please summarise this transcript for me in a \
#         few sentences: " + transcript + "\n\nTl;dr"
#         summary = summarize_yt_script_with_gpt3(task)
#         summary = summary.strip(" :-")
#         time.sleep(limiter)
#         return summary


# def get_most_popular_video_transcripts_by_topic(topic, amount):
#     parser = YoutubeParser(topic, amount)
#     return parser.execute()

def get_videos_by_topic(topics, number):
    return []