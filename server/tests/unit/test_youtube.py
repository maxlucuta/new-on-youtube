import pytest 
from website.utilities import youtube as yt

def test_youtube_api():
    """Test YouTube API methods are correctly
       processing requests.
    """
    topic, count = "football", 1
    response = yt.get_most_popular_video_transcripts_by_topic(topic, count)

    for data in response:
        key = data.get('keyword')
        video = data.get('video_title')
        channel = data.get('channel_name')
        summary = data.get('summary')

        assert key and video and channel and summary
        assert len(data) == 4
    
    assert len(response) == count
