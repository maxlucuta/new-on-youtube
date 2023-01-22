"""Important information:

Implementation routes front-end GET requests to /request,
it is the front-end developers responsibility to ensure
that the URL Query contains both topic=x and amount=y, 
otherwise an error code will be returned.
"""
from flask import Blueprint, request, abort
from website.models import establish_connection, query_yt_videos
from werkzeug.exceptions import HTTPException

request_blueprint = Blueprint("request_blueprint", __name__)
session = None

@request_blueprint.errorhandler(400)
def bad_request(e):
	""" Handles HTTPException code 400.

		Returns: dict containing error description
		         and status code.
	"""
	return {'ERROR' : 'GET Request failed.', 'STATUS CODE' : 400 }

@request_blueprint.errorhandler(404)
def not_found(e):
	""" Handles HTTPException code 404.

		Returns: dict containing error description
		         and status code.
	"""
	return {'ERROR' : 'Topic not found.', 'STATUS CODE' : 404 }

@request_blueprint.errorhandler(408)
def timeout(e):
	""" Handles HTTPException code 408.

		Returns: dict containing error description
		         and status code.
	"""
	return {'ERROR' : 'Database connection timed out.', 'STATUS CODE' : 408 }

@request_blueprint.errorhandler(417)
def query_failure(e):
	""" Handles HTTPException code 417.

		Returns: dict containing error description
		         and status code.
	"""
	return {'ERROR' : 'Unable to fetch request from database.', 'STATUS CODE' : 417 }

@request_blueprint.errorhandler(500)
def server_error(e):
	""" Handles HTTPException code 500.

		Returns: dict containing error description
		         and status code.
	"""
	return {'ERROR' : 'Database connection failiure.', 'STATUS CODE' : 500 }

def valid_get_request(topic, amount):
	"""Checks if the GET request params are valid.

	Args:
		topic: string denoting topic to query.
		amount: int denoting number of expected responses.
			
	Returns:
		True if request is valid.
		False if request is invalid.
	"""
	if not topic or not amount:
		return False

	if not topic.isalpha() or not amount.isdigit(): 
		return False

	if 0 >= int(amount) or int(amount) > 20:
		return False
		
	return True

def valid_query_response(topic_summaries, amount):
	"""Checks if the GET response satisfies the request.

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
		if query_response.get("ERROR") or len(query_response) != 3:
			abort(404)

		video_title = query_response.get('video_title')
		channel_name = query_response.get('channel_name')
		summary = query_response.get('summary')

		if not video_title or not channel_name or not summary:
			return False

	return len(topic_summaries) == amount


@request_blueprint.route("/", methods=['GET'])
@request_blueprint.route("/home", methods=['GET'])
@request_blueprint.route("/request", methods=['GET'])
def request_summary():
	""" Retrieves summarised transcripts for a topic.

	Args:
		topic: GET request -> topic extracted through URL
		       query parameters as string.
		amount: Included in GET URL query parameters, 
		 	   denotes number of summaries to be retrieved.

	Returns:
		summary: { video : vid_title, channel : channel_name, summary : s }
				dict with key : val bring string : string. Dict is of k * 3
				elements where k is number of videos in amount.

	Raises:
		HTTPException 400 / 404 / 408 / 417 / 500
	"""
	topic = request.args.get('topic')
	amount = request.args.get('amount')
	global session

	if not session:
		session = establish_connection()

	if not valid_get_request(topic, amount):
		abort(400)
	
	topic_summaries = query_yt_videos(topic, int(amount), session)

	if not valid_query_response(topic_summaries, int(amount)):
		abort(417)
	
	return topic_summaries











