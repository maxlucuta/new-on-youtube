from youtube_transcript_api import YouTubeTranscriptApi
from .gpt3 import summarize_yt_script_with_gpt3
import googleapiclient.discovery as googleapi
import requests, time


API_KEY = "AIzaSyCEYn_Co51eJlG5sCbzVbPQ9HQn-RHxRms"
youtube = googleapi.build("youtube", "v3", developerKey = API_KEY)


def get_most_popular_video_transcripts_by_topic(topic, result_num, fast_summarizer=False):
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
    instruction = "Please summarise this transcript for me in a few sentences: "

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

        transcript = instruction + generate_transcript(video_id) + "\n\nTl;dr"
        summary = summarize_yt_script_with_gpt3(transcript)
        formatted_request_response.append({'keyword' : topic, 
                                           'video_title' : video_title,
                                           'channel_name' : channel_name,
                                           'summary' : summary})
        
        if not fast_summarizer: time.sleep(5)

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

def parse_video_endpoint_response(response):
    """ Parses the 'items' list in the response returned by the YouTube API 
    'Videos:list' endpoint, including treating missing values. This is used as 
    a helper function by multiple functions that call this endpoint. 
    
    Args:
        response: dict -> a dict containing a YouTube video.list API response.
        
    Returns:
        parsed_item_details: [{dict}] -> A list of flattened dicts 
        containing information for each video item. 
    """
    parsed_item_details = []
    
    for response_item in response["items"]:
        video_id = response_item["id"]
        
        video_overview = response_item.get("snippet", {})
        content_details = response_item.get("contentDetails", {})
        topics = response_item.get("topicDetails", {})
        statistics = response_item.get("statistics", {})
        
        item_details = {'video_id': video_id,
                        'video_name' : video_overview.get('title'),
                        'channel_id' : video_overview.get('channelId'),
                        'channel_name' : video_overview.get('channelTitle'),
                        'video_description' : video_overview.get('description'),
                        'video_tags' : video_overview.get('tags', []),
                        'published_at' : video_overview.get('publishedAt'),
                        'video_topics' : topics.get('topicCategories', []),
                        'views' : statistics.get('viewCount'),
                        'likes' : statistics.get('likeCount'),
                        'quality' : content_details.get('definition'),
                        'duration' : content_details.get('duration')
                        }
        parsed_item_details.append(item_details)
        
    return parsed_item_details
    

def get_video_information_by_id(video_ids):
    """ Calls the YouTube API 'Videos:list' endpoint to retreive information 
    on a specified list of videos, returning the processed information in a 
    format to be consumed by database.py.
    
    Args:
        video_ids: list -> a list of YouTube video ids (maximum 50).
        
    Returns:
        [{dict}] -> A list of flattened dicts containing information for 
        each video item in the response.
    """
    global youtube
    
    information_sections = ["snippet", "contentDetails", "statistics",
                            "topicDetails"]
    
    number_videos = len(video_ids)
    request = youtube.videos().list(part = ",".join(information_sections), 
                                    id = ",".join(video_ids), 
                                    regionCode = "gb",
                                    maxResults = number_videos)
    response = request.execute()
        
    return parse_video_endpoint_response(response)


def get_charting_video_information(result_num):
    """ Calls the YouTube API video.list endpoint to retreive information on
    currently charting videos (i.e. those shown on the trending page).
    Currently accepts a maximum of 50 IDs.
    
    Args:
        result_num: int -> number of videos to return (maximum 50).
        
    Returns:
        [{dict}] -> A list of flattened dicts containing information for 
        each video item.
    """
    global youtube
    
    information_sections = ["snippet", "contentDetails", "statistics",
                            "topicDetails"]

    request = youtube.videos().list(part = ",".join(information_sections),
                                    chart = "mostPopular", regionCode = "gb",
                                    maxResults = result_num)
    response = request.execute()
    
    return parse_video_endpoint_response(response)