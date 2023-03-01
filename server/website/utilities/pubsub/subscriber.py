from os import environ
from google.cloud import pubsub_v1
from ..youtube_scraper_lib.youtube import (
    get_most_popular_video_transcripts_by_topic
)
from ..database import insert_video
from .logs.message_logger import Logger

SUBSCRIBER_PATH = "projects/new-on-youtube-375417/subscriptions/gpt-tasks-sub"


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

    def callback(self, message: object):
        """Processes pulled message from Subscriber queue and calls
        database methods to insert into DB.

        Args:
            message (pubsub.message): connection to substriber client
            and an instance of the subscriber session.
        """

        topic = message.attributes.get('search_term')
        amount = int(message.attributes.get('amount'))
        print(f"{topic} recieved!", flush=True)
        log = topic + "," + str(amount)

        if self.logger.get(log):
            print("Duplicate message found!", flush=True)
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
        return

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
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()
        return


def run_background_task():
    subscriber = Subscriber()
    subscriber.process_tasks()
