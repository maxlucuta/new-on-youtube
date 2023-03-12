from os import environ
from google.cloud import pubsub_v1
from .logs.message_logger import Logger

TOPIC_PATH = "projects/new-on-youtube-375417/topics/gpt-tasks"


class Publisher:
    """Publisher class for Google PubSub."""

    def __init__(self, topic=TOPIC_PATH):
        """Constructs a Publisher object.

        Args:
            topic (str, optional): path to Google PubSub topic
        """

        self.publisher = self.publisher_connect()
        self.logger = Logger("publisher")
        self.topic = topic

    def publisher_connect(self):
        """Connects to Google PubSub Publisher Client

        Returns:
            Publisher: Obj, connection to publisher client
            and an instance of the publisher session.
        """

        environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
            "./website/utilities//pubsub/pubsub_privatekey.json"
        publisher = pubsub_v1.PublisherClient()
        return publisher

    def create_task(self, topic: str, amount: str):
        """Creates a GPT3 processing task that is added to
        a cloud based PubSub queue.

        Args:
            topic (string): topic to query from YT API.
            amount (string): number of query results.
        """

        data = "GPT-Job"
        data = data.encode("utf-8")
        log = topic + ',' + amount
        if self.logger.get(log):
            return
        if int(amount) >= 5:
            self.logger(log)
        attributes = {'search_term': topic, 'amount': amount}
        self.publisher.publish(self.topic, data, **attributes)
