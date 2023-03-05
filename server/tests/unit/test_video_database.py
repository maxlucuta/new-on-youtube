from website.utilities import database as db


def test_db_contains_video_returns_valid_response():
    assert (db.db_contains_video('f1', 'aouCUd_NcmE'))


# remove when working
# def test_get_recommended_videos_returns_valid_response():
#   assert (db.get_recommended_videos('devuser4', 10))


def test_query_videos_returns_valid_response():
    assert (db.query_videos(['f1'], 5, "Random"))
