"""Important information:

Implementation routes front-end POST requests to /request,
it is the front-end developers responsibility to ensure
that the request contains both topic = x and amount = y,
otherwise an error code will be returned.
"""
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required
from .utilities.database import query_users
from .utilities.database import set_user_topics
from .utilities.database import query_videos
from .utilities.database import get_recommended_videos
from .utilities.database import add_videos_to_queue
from .utilities.database import add_watched_video
from .utilities.database import add_more_videos_to_queue
from .utilities.database import delete_database_entry
from .utilities.database import insert_video
from .utilities.database import query_random_videos
from .utilities.youtube_scraper_lib.youtube import get_updated_metadata_by_id

request_blueprint = Blueprint("request_blueprint", __name__)


@request_blueprint.errorhandler(400)
def bad_request(e):
    """ Handles HTTPException code 400.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 400,
        'description': 'POST Request failed.',
        'results': []
    }


@request_blueprint.errorhandler(404)
def not_found(e):
    """ Handles HTTPException code 404.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 404,
        'description': 'Topic not found.',
        'results': []
    }


@request_blueprint.errorhandler(408)
def timeout(e):
    """ Handles HTTPException code 408.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 408,
        'description': 'Database connection timed out.',
        'results': []
    }


@request_blueprint.errorhandler(417)
def query_failure(e):
    """ Handles HTTPException code 417.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 417,
        'description': 'Unable to fetch request from database.',
        'results': []
    }


@request_blueprint.errorhandler(500)
def server_error(e):
    """ Handles HTTPException code 500.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 500,
        'description': 'Database connection failiure.',
        'results': []
    }


def valid_video_request(topics, amount):
    """Checks if the POST request params are valid.
    Args:
            topic: string denoting topic to query.
            amount: int denoting number of expected responses.

    Returns:
            True if request is valid.
            False if request is invalid.
    """
    if not topics or not amount:
        return False

    if not str(amount).isdigit() or \
            0 >= int(amount) or int(amount) > 20:
        return False

    return True


def valid_video_response(response, amount):
    """Checks if the POST response satisfies the request.
    Args:
            topic_summaries: [{dict}] containing query response.
            amount: int denoting number of expected responses.

    Returns:
            True if response is valid.
            False if response is incomplete.
    """
    keys = ['video_title', 'views', 'summary', 'likes',
            'published_at', 'channel_name']
    for result in response:
        if not all(x in result for x in keys):
            return False
    return len(response) <= amount


@request_blueprint.route("/", methods=['POST'])
@request_blueprint.route("/home", methods=['POST'])
@request_blueprint.route("/request", methods=['POST'])
def request_videos():
    """ Retrieves summarised transcripts for a topic.
    Args:
            topic: GET request -> topic extracted through URL
                       query parameters as string.
            amount: Included in GET URL query parameters,
                       denotes number of summaries to be retrieved.
    Returns:
            summary: { video : vid_title, channel : channel_name, summary : s }
                            dict with key : val bring string : string.
                            Dict is of k * 3 elements where k is number of
                            videos in amount.
    Raises:
            HTTPException 400 / 404 / 408 / 417 / 500
    """

    body = request.get_json()
    try:
        topics = body["topics"]
        amount = body["amount"]
    except KeyError:
        return {'status_code': 400, 'description': 'Missing payload fields'}

    if not valid_video_request(topics, amount):
        return {'status_code': 400, 'description': 'Invalid payload fields'}

    response = query_videos(topics, amount, "Random")

    if not valid_video_response(response, int(amount)):
        abort(417)

    return {'status_code': 200, 'description': 'Ok.', 'results': response}


@request_blueprint.route("/user_request", methods=['POST'])
@jwt_required()
def request_user_videos():
    """ Retrieves sorted summarised transcripts for a list of topics.
    Args:
            json: POST request -> username, topics, and sorted method extracted
                   from json
    Returns:
            response: List of dicts, one for each returned video. Each of
                      which contains 'keyword', 'likes', 'video_title',
                      'published_at', 'video_id', 'summary', 'channel_name'
    Raises:
            HTTPException 400 / 404 / 408 / 417 / 500
    """

    body = request.get_json()
    try:
        username = body["username"]
        amount = body["amount"]
        sort_by = body["sort_by"]
    except KeyError:
        return {'status_code': 400,
                'description': 'Missing payload fields'}

    user = query_users(username)
    if not user:
        return {'status_code': 500,
                'description':
                'username not found in database'}

    if sort_by == "Recommended":
        response = get_recommended_videos(username, amount)
    else:
        topics = user.topics
        if not valid_video_request(topics, amount):
            return {'status_code': 400,
                    'description':
                    'Invalid payload fields'}
        response = query_videos(topics, amount, sort_by)

    if not valid_video_response(response, int(amount)):
        abort(417)

    return {'status_code': 200,
            'description': 'Ok.',
            'results': response}


@request_blueprint.route("/get_user_topics", methods=['POST'])
@jwt_required()
def get_user_topics():
    try:
        username = request.json["username"]
    except KeyError:
        return {'status_code': 400,
                'description':
                'Missing payload fields'}
    user = query_users(username)
    if not user:
        return {'status_code': 500,
                'description': 'username not found in database'}
    results = user.topics
    return {'status_code': 200,
            'description': 'Ok.',
            'results': results}


@request_blueprint.route("/update_user_topics", methods=['POST'])
@jwt_required()
def update_user_topics():
    try:
        username = request.json["username"]
        topics = request.json["topics"]
    except KeyError:
        return {'status_code': 400,
                'description': 'Missing payload fields'}
    if not set_user_topics(username, topics):
        return {'status_code': 500,
                'description': 'database update failed'}
    add_videos_to_queue(topics)
    return {'status_code': 200, 'description': 'Ok.'}


@request_blueprint.route("/update_user_watched_videos", methods=['POST'])
@jwt_required()
def update_user_watched_videos():
    try:
        username = request.json["username"]
        topic = request.json["keyword"]
        video_id = request.json["video_id"]
    except KeyError:
        return {'status_code': 400,
                'description': 'Missing payload fields'}

    add_more_videos_to_queue(topic, 2)

    if not add_watched_video(username, video_id):
        return {'status_code': 500,
                'description': 'database update failed'}
    return {'status_code': 200, 'description': 'Ok.'}


@request_blueprint.route("/update_me_daddy", methods=['GET'])
def run_database_update_job():
    """Hidden endpoint for running data update jobs, this method
       will fetch a number of entires from the database and update
       them with the latest metadata.
    """

    to_update = query_random_videos(200)
    for response in to_update:
        get_newest_data = get_updated_metadata_by_id(response['video_id'])
        if not get_newest_data:
            continue
        delete_database_entry(response)
        video_name = response['video_title']
        response['video_tags'] = response['video_tags'].split(",")
        del response['video_title']
        del response['likes']
        del response['views']
        del response['published_at']
        response.update(get_newest_data)
        response['video_name'] = video_name
        insert_video(response)

    return {'status_code': 200, 'description': 'Ok.'}
