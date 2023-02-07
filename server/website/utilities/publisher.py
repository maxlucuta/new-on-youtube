from google.cloud import pubsub_v1 as pubsub
from os import environ

TOPIC_PATH = "projects/new-on-youtube-375417/topics/gpt-tasks"


def publisher_connect():
    """Connects to Google PubSub Publisher Client

    Returns:
        Publisher: Obj, connection to publisher client
        and an instance of the publisher session.
    """
    environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        "./website/utilities/pubsub_privatekey.json"
    publisher = pubsub.PublisherClient()
    return publisher


def create_task(topic, amount):
    """Creates a GPT3 processing task that is added to
       a cloud based PubSub queue.

    Args:
        topic (string): topic to query from YT API.
        amount (string): number of query results.
    """
    global TOPIC_PATH
    publisher = publisher_connect()
    data = "GPT-Job"
    data = data.encode("utf-8")
    attributes = {'search_term': topic, 'amount': amount}
    # future = publisher.publish(TOPIC_PATH, data, **attributes)
    publisher.publish(TOPIC_PATH, data, **attributes)

    return
