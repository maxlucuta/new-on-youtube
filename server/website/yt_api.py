from youtube_transcript_api import YouTubeTranscriptApi
from gpt_api import summarize_yt_script_with_gpt3
import googleapiclient.discovery as googleapi
import requests


API_KEY = "AIzaSyCEYn_Co51eJlG5sCbzVbPQ9HQn-RHxRms"
youtube = googleapi.build("youtube", "v3", developerKey = API_KEY)


def get_most_popular_video_transcripts_by_topic(topic, result_num):
    """ Calls youtube data api to fetch metadata for videos of
        the specific topic, returning processed data to be 
        stored in models.py database.

        Args:
            topic: string -> video topic
            result_num: int -> number of videos to query

        Returns:
            transcript: [{dict}] in the format found in models.py
    """
    global youtube
    formatted_request_response = []

    request = youtube.search().list(part = "snippet", q = topic,
                                    maxResults = result_num, 
                                    order = "viewCount", type = "video",
                                    regionCode = "gb", safeSearch = "moderate",
                                    videoDuration = "short",
                                    videoCaption = "closedCaption")

    response = request.execute()

    for item in response['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        channel_name = item['snippet']['channelTitle']

        transcript = generate_transcript(video_id) + "\n\nTl;dr"
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

        