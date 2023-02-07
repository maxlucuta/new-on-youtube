from website.utilities import youtube as yt


def test_youtube_api():
    """Test YouTube API methods are correctly
       processing requests.
    """
    topic, count = "football", 1
    response = yt.get_most_popular_video_transcripts_by_topic(topic, count)

    for data in response:
        key = data.get('keyword')
        video = data.get('video_name')
        channel = data.get('channel_name')
        summary = data.get('summary')

        assert key and video and channel and summary

    assert len(response) == count


def test_youtube_video_endpoint_by_id():

    video_ids = ["DbqPrMTrQHc", "YOts1Crp21A", "BYVZh5kqaFg"]
    response = yt.get_video_information_by_id(video_ids,
                                              fast_summarizer=False,
                                              include_summary=False,
                                              pause_length=1)

    for data in response:
        # Test mandatory response data is not None
        assert data.get('video_id')
        assert data.get('video_name')

    assert len(response) == len(video_ids)
