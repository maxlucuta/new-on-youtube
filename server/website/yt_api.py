from youtube_transcript_api import YouTubeTranscriptApi
from gpt_api import summarize_yt_script_with_gpt3
import googleapiclient.discovery
import requests



API_SERVICE = "youtube"
API_VERSION = "v3"
API_KEY = "AIzaSyCEYn_Co51eJlG5sCbzVbPQ9HQn-RHxRms"

api_results_per_page = 1
search_terms = "football"

youtube = googleapiclient.discovery.build(
    API_SERVICE, API_VERSION, developerKey = API_KEY)


def get_most_popular_video_transcripts_by_topic(topic, result_num):

    global youtube
    formatted_request_response = []

    request = youtube.search().list(part = "snippet", q = search_terms,
                                    maxResults = api_results_per_page, 
                                    order = "viewCount", type = "video",
                                    regionCode = "gb", safeSearch = "moderate",
                                    videoDuration = "medium",
                                    videoCaption = "closedCaption")

    response = request.execute()

    for item in response['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        channel_name = item['snippet']['channelTitle']

        transcript = generate_transcript(video_id)
        print(transcript)
        summary = summarize_yt_script_with_gpt3(transcript)
        formatted_request_response.append({'video_title' : video_title,
                                           'channel_name' : channel_name,
                                           'summary' : summary})

    return formatted_request_response


def generate_transcript(key):
    """ Calls youtube_transcript api to return a transcript 
        for a specific video.

        Args:
            key: string -> unique key for video.

        Returns:
            transcript: string -> transcript for the video.
    """
    raw_transcript = YouTubeTranscriptApi.get_transcript(key)
    final_transcript = []

    for text in raw_transcript:
        word = text.get('text')
        if not word or word == '[Music]':
            continue
        final_transcript.append(word)
    
    return " ".join(final_transcript)

print(get_most_popular_video_transcripts_by_topic("football", 1))
        