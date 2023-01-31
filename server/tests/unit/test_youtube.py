import pytest 
from website.utilities import youtube as yt

def test_youtube_api():

    topic = "football"
    count = 1

    response = yt.get_most_popular_video_transcripts_by_topic(topic, count)

    for data in response:
        key = data.get('keyword')
        video = data.get('video_title')
        channel = data.get('channel_name')
        summary = data.get('summary')

        assert key and video and channel and summary
        assert len(data) == 4
    
    assert len(response) == count

def test_youtube_video_endpoint_by_id():
    
    video_ids = ["DbqPrMTrQHc", "YOts1Crp21A", "BYVZh5kqaFg"]
    response = get_video_information_by_id(video_ids)

    for data in response:
        ## Test mandatory response data is not None
        assert data.get('video_id')
        assert data.get('video_name')

    assert len(response) == len(video_ids)

def test_youtube_video_endpoint_charts():
    
    count = 3
    response = get_charting_video_information(count)

    for data in response:
        ## Test mandatory response data is not None
        assert data.get('video_id')
        assert data.get('video_name')

    assert len(response) == count