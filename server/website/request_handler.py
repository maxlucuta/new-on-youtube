"""Important information:

Implementation routes front-end POST requests to /request,
it is the front-end developers responsibility to ensure
that the request contains both topic=x and amount=y,
otherwise an error code will be returned.
"""
from flask import Blueprint, request, abort
from .utilities.database import establish_connection, query_yt_videos_list
from .utilities.youtube import get_popular_topics
# from werkzeug.exceptions import HTTPException

request_blueprint = Blueprint("request_blueprint", __name__)
session = None


@request_blueprint.errorhandler(400)
def bad_request(e):
    """ Handles HTTPException code 400.

        Returns: dict containing error description
                 and status code.
    """
    return {'ERROR': 'GET Request failed.', 'STATUS CODE': 400}


@request_blueprint.errorhandler(404)
def not_found(e):
    """ Handles HTTPException code 404.

        Returns: dict containing error description
                 and status code.
    """
    return {'ERROR': 'Topic not found.', 'STATUS CODE': 404}


@request_blueprint.errorhandler(408)
def timeout(e):
    """ Handles HTTPException code 408.

        Returns: dict containing error description
                 and status code.
    """
    return {'ERROR': 'Database connection timed out.', 'STATUS CODE': 408}


@request_blueprint.errorhandler(417)
def query_failure(e):
    """ Handles HTTPException code 417.

        Returns: dict containing error description
                 and status code.
    """
    return {'ERROR': 'Unable to fetch request from database.',
            'STATUS CODE': 417}


@request_blueprint.errorhandler(500)
def server_error(e):
    """ Handles HTTPException code 500.

        Returns: dict containing error description
                 and status code.
    """
    return {'ERROR': 'Database connection failiure.', 'STATUS CODE': 500}


def valid_get_request(topics, amount):
    """Checks if the POST request params are valid.

    Args:
        topic: string denoting topic to query.
        amount: int denoting number of expected responses.

    Returns:
        True if request is valid.
        False if request is invalid.
    """
    print(topics, amount)
    if not topics or not amount:
        return False

    if 0 >= int(amount) or int(amount) > 20:
        return False

    return True


def valid_query_response(topic_summaries, amount):
    """Checks if the POST response satisfies the request.

    Args:
        topic_summaries: [{dict}] containing query response.
        amount: int denoting number of expected responses.

    Returns:
        True if response is valid.
        False if response is incomplete.

    Raises:
        HTTPException 404.
    """
    for query_response in topic_summaries:
        if len(query_response) != 3:
            print("bad query reponse fields", query_response)
            abort(404)

        title = query_response.get('title')
        id = query_response.get('id')
        description = query_response.get('description')

        if not title or not id or not description:
            print("bad query reponse fields", query_response)
            return False

    return True


@request_blueprint.route("/", methods=['POST'])
@request_blueprint.route("/home", methods=['POST'])
@request_blueprint.route("/request", methods=['POST'])
def request_summary():
    """ Retrieves summarised transcripts for a topic.

    Args:
        topic: POST request -> topic extracted through POST
               query parameters as string.
        amount: Included in POST query parameters, denotes
               number of summaries to be retrieved.

    Returns:
        summary: { video : vid_title, channel : channel_name, summary : s }
                dict with key : val bring string : string. Dict is of k * 3
                elements where k is number of videos in amount.

    Raises:
        HTTPException 400 / 404 / 408 / 417 / 500
    """
    topics = request.json["topics"]
    amount = request.json["amount"]
    global session

    if not session:
        print("Session could not be established")
        session = establish_connection()

    if not valid_get_request(topics, amount):
        print("Invalid Request", topics, amount)
        abort(400)

    topic_summaries = query_yt_videos_list(topics, int(amount), session)

    if not valid_query_response(topic_summaries, int(amount)):
        print("Invalid Database Query", topic_summaries, amount)
        abort(417)

    print(topics)
    return topic_summaries


@request_blueprint.route("/popular_topics", methods=['get'])
def popular_topics():
    get_popular_topics()
    return ["elephants"]

@request_blueprint.route("/popular_videos", methods=['get'])
def popular_videos():
    return [{ "id": "plv506632yo", "descripion": "spongebob", "title": "Funny moments from ze sponge" }]
