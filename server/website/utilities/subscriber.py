from google.cloud import pubsub_v1 as pubsub
from concurrent.futures import TimeoutError
from youtube_transcript_api import NoTranscriptFound
from .youtube import get_most_popular_video_transcripts_by_topic
from .database import insert_into_DB, establish_connection
from os import environ
import time

SUBSCRIBER_PATH = "projects/new-on-youtube-375417/subscriptions/gpt-tasks-sub"
SESSION = None

def subscriber_connect():
    """Connects to Google PubSub Subscriber Client

    Returns:
        Subscriber: Obj, connection to substriber client
        and an instance of the subscriber session.
    """
    environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./website/utilities/pubsub_privatekey.json"
    subscriber = pubsub.SubscriberClient()
    return subscriber

def callback(message):
    """Processes pulled message from Subscriber queue and calls 
       database methods to insert into DB.

    Args:
        message (pubsub.message): connection to substriber client
        and an instance of the subscriber session.
    """
    topic = message.attributes.get('search_term')
    amount = message.attributes.get('amount')
    
    try:
        processed_task = get_most_popular_video_transcripts_by_topic(topic, amount)
    except NoTranscriptFound:
        message.ack()
        return
 
    global SESSION
    if not SESSION:
        SESSION = establish_connection()

    for data in processed_task:
        insert_into_DB(data, SESSION)

    message.ack()
    return

def process_tasks():
    """Stream processes subsriber content indefinitely until
       current thread is terminated.
    """
    global SUBSCRIBER_PATH
    subscriber = subscriber_connect()
    flow_control = pubsub.types.FlowControl(max_messages=10)

    streaming_pull_future = subscriber.subscribe(
    SUBSCRIBER_PATH, callback=callback, flow_control=flow_control)

    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
    return




