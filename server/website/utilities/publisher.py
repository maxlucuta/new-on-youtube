from google.cloud import pubsub_v1 as pubsub
from os import environ
from .logs.message_logger import Logger

TOPIC_PATH = "projects/new-on-youtube-375417/topics/gpt-tasks"

class Publisher:
    def __init__(self, topic=TOPIC_PATH):
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
            "./website/utilities/pubsub_privatekey.json"
        publisher = pubsub.PublisherClient()
        return publisher


    def create_task(self, topic, amount):
        """Creates a GPT3 processing task that is added to
        a cloud based PubSub queue.

        Args:
            topic (string): topic to query from YT API.
            amount (string): number of query results.
        """
        data = "GPT-Job"
        data = data.encode("utf-8")
        attributes = {'search_term': topic, 'amount': amount}
        if self.logger(attributes):
            return
        self.logger.add(attributes)
        self.publisher.publish(self.topic, data, **attributes)
        return
