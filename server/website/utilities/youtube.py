from youtube_transcript_api import YouTubeTranscriptApi
from .gpt3 import summarize_yt_script_with_gpt3
import googleapiclient.discovery as googleapi
import requests, time


API_KEY = "AIzaSyCEYn_Co51eJlG5sCbzVbPQ9HQn-RHxRms"
youtube = googleapi.build("youtube", "v3", developerKey = API_KEY)


def get_most_popular_video_transcripts_by_topic(topic, videos_requested, fast_summarizer=False, include_summary=True, pause_length=1):
    """Calls youtube data api to fetch metadata for videos of
    the specific topic, returning processed data to be stored in the database.
    A maximum of 50 videos can be fetched from the API per call.
    Requests for a larger number of videos will make multiple calls to the API.

    Args:
        topic: string -> video topic
        result_num: int -> number of videos to query
        fast_summarizer: bool -> will use a summarizer model when True, GPT-3 API call when False
        include_summary: bool -> when False only video information will be fetched, no summary will be generated
        pause_length: int -> the time in seconds to wait between calls to GPT-3 API.

    Returns:
        results: [{dict}] in the format found in models.py
    """
    results = []

    ## Note max_requests of 50 is set by the YouTube API
    max_requests = 50
    
    if videos_requested > max_requests:
        videos_to_request = max_requests
    else:
        videos_to_request = videos_requested
        
    remaining_videos = videos_requested - max_requests
    
    current_request = get_search_endpoint_ids(topic, videos_to_request, "")
    video_ids = current_request['video_ids']
    next_page = current_request.get('next_page')
    
    while(remaining_videos > 0):
        if remaining_videos > max_requests:
            videos_to_request = max_requests
        else:
            videos_to_request = remaining_videos
            
        current_request = get_search_endpoint_ids(topic, videos_to_request, next_page)
        video_ids.extend(current_request['video_ids'])
        next_page = current_request.get('next_page')
        remaining_videos -= max_requests
    
    ## Check fetched videos are unique as API pagination can be inconsistent
    video_ids = list(set(video_ids))
    
    ## Retrieve the video information by id in groups of max size 50
    while video_ids:
        i = len(video_ids) - max_requests
        results.extend(get_video_information_by_id(video_ids[i:], fast_summarizer, include_summary, pause_length))
        del video_ids[i:]

    for result in results:
        result['keyword'] = topic
    
    return results

def get_search_endpoint_ids(topic, num_videos, page_token):
    """Gets video IDs for a given topic from the YouTube Videos:List API endpoint.
    Accepts a 'page_token' parameter to allow for paginated results
    
    Args:
        topic: string -> video topic
        num_videos: int -> number of videos to query (maximum 50)
        page_token: string -> token for YouTube API pagination. 
            An empty string returns the first page. 

    Returns:
        results: [{dict}] in the format found in models.py
    
    """
    request = youtube.search().list(part = "snippet", q = topic,
                                    maxResults = num_videos, 
                                    order = "viewCount", pageToken = page_token,
                                    type = "video", regionCode = "gb", 
                                    safeSearch = "moderate", 
                                    videoDuration = "short",
                                    videoCaption = "closedCaption")
    
    response = request.execute()
    
    video_ids = [item['id']['videoId'] for item in response['items']]
    
    return {'video_ids': video_ids, 'next_page': response['nextPageToken']}

def generate_transcript(key):
    """ Calls youtube_transcript api to return a transcript 
        for a specific video.

        Args:
            key: string -> unique key for video.

        Returns:
            transcript: string -> transcript for the video.
    """
    try:
        raw_transcript = YouTubeTranscriptApi.get_transcript(key, languages=['en', 'en-GB'])
        final_transcript = []
    
        for text in raw_transcript:
            word = text.get('text')
            if not word or word == '[Music]':
                continue
            final_transcript.append(word)
        return " ".join(final_transcript)
    
    except YouTubeTranscriptApi.NoTranscriptFound:
        return ""

def parse_video_endpoint_response(response_item):
    """ Parses the 'items' list in the response returned by the YouTube API 
    'Videos:list' endpoint, including treating missing values. This is used as 
    a helper function by multiple functions that call this endpoint. 
    
    Args:
        response: dict -> a dict containing a YouTube video.list API response.
        
    Returns:
        parsed_item_details: [{dict}] -> A list of flattened dicts 
        containing information for each video item. 
    """

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

        
    return item_details
    

def get_video_information_by_id(video_ids, fast_summarizer, include_summary, pause_length):
    """ Calls the YouTube API 'Videos:list' endpoint to retreive information 
    on a specified list of videos, returning the processed information in a 
    format to be consumed by database.py.
    
    Args:
        video_ids: list -> a list of YouTube video ids (maximum 50).
        fast_summarizer: bool -> will use a summarizer model when True, GPT-3 API call when False
        include_summary: bool -> when False only video information will be fetched, no summary will be generated
        pause_length: int -> the time in seconds to wait between calls to GPT-3 API.
        
    Returns:
        [{dict}] -> A list of flattened dicts containing information for 
            each video item in the response.
    """
    global youtube
    
    full_video_information = []
    instruction = "Please summarise this transcript for me in a few sentences: "
    
    information_sections = ["snippet", "contentDetails", "statistics",
                            "topicDetails"]
    
    number_videos = len(video_ids)
    request = youtube.videos().list(part = ",".join(information_sections), 
                                    id = ",".join(video_ids), 
                                    regionCode = "gb",
                                    maxResults = number_videos)
    
    response = request.execute()
    
    for item in response['items']:
        video_information = parse_video_endpoint_response(item)
        
        if include_summary:
            transcript = generate_transcript(video_information['video_id'])
            
            ## Errors in transcript generation will return an empty string
            ## In these cases no video information record will be created
            if transcript:
                gpt_prompt = instruction + transcript + "\n\nTl;dr"
                video_information['summary'] = summarize_yt_script_with_gpt3(gpt_prompt)
                
                ## Remove common prefixes on GPT-3 outputs
                video_information['summary'] = video_information['summary'].strip(" :-")
                
                
                if not fast_summarizer:
                    time.sleep(pause_length)
        else:
            video_information['summary'] = ""
            
        full_video_information.append(video_information)
            
    return full_video_information