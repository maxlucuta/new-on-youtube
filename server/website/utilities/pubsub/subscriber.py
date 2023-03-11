from os import environ
from functools import wraps
from multiprocessing import current_process
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.exceptions import AcknowledgeError
from ..youtube_scraper_lib.youtube import (
    get_most_popular_video_transcripts_by_topic
)
from ..database import insert_video, create_session
from .logs.message_logger import Logger

SUBSCRIBER_PATH = "projects/new-on-youtube-375417/subscriptions/gpt-tasks-sub"


def ignore_ack_errors(func: callable) -> callable:
    """Wrapper function to supress AcknowledgeError bug in Google PubSub.
       Prevents long stack trace being shown in logs console."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AcknowledgeError, ValueError):
            print("Ack error handled!", flush=True)
    return inner


class Subscriber:
    """Subscriber class for Google PubSub."""

    def __init__(self, topic: str = SUBSCRIBER_PATH):
        """Constructs a Subscriber object.

        Args:
            topic (str, optional): path to Google PubSub topic
        """

        self.subscriber = self.subscriber_connect()
        self.logger = Logger("subscriber")
        self.topic = topic

    def subscriber_connect(self) -> object:
        """Connects to Google PubSub Subscriber Client

        Returns:
            Subscriber: Obj, connection to substriber client
            and an instance of the subscriber session.
        """

        environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
            "./website/utilities/pubsub/pubsub_privatekey.json"
        subscriber = pubsub_v1.SubscriberClient()
        return subscriber

    @ignore_ack_errors
    def callback(self, message: object):
        """Processes pulled message from Subscriber queue and calls
        database methods to insert into DB.

        Args:
            message (pubsub.message): connection to substriber client
            and an instance of the subscriber session.
        """

        topic = message.attributes.get('search_term')
        amount = int(message.attributes.get('amount'))
        print(f"{topic} recieved by " +
              current_process().name + "!", flush=True)
        log = topic + "," + str(amount)

        if self.logger.get(log):
            message.ack()
            return
        else:
            self.logger(log)

        processed_task = get_most_popular_video_transcripts_by_topic(
            topic, int(amount))

        for data in processed_task:
            print('subscriber running insert into db', flush=True)
            insert_video(data)

        print(f"{topic} processed!", flush=True)
        message.ack()

    def process_tasks(self):
        """Stream processes subsriber content indefinitely until
        current thread is terminated.
        """

        flow_control = pubsub_v1.types.FlowControl(max_messages=1)
        streaming_pull_future = self.subscriber.subscribe(
            self.topic,
            callback=self.callback, flow_control=flow_control)
        with self.subscriber:
            try:
                streaming_pull_future.result()
            except Exception:
                streaming_pull_future.cancel()
                streaming_pull_future.result()


def run_background_task():
    """API for daemon thread background processing."""

    create_session()
    subscriber = Subscriber()
    subscriber.process_tasks()
