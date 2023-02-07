from website.utilities import youtube as yt
import googleapiclient.errors as googleapi_errors


def test_youtube_api():
    """Test YouTube API methods are correctly
       processing requests.
    """

    topic, count = "football", 2

    try:
        response = yt.get_most_popular_video_transcripts_by_topic(topic, count)

        for data in response:
            key = data.get('keyword')
            video = data.get('video_name')
            channel = data.get('channel_name')
            summary = data.get('summary')

            assert key and video and channel and summary

        assert len(response) == count

    except googleapi_errors.HttpError as err:
        if err.resp.status == 403:
            print("Warning: Daily YouTube API quota exceeded.")
