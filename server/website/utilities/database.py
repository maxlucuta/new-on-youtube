"""
This file contains all functions related to database operations for the
applications Apache Cassandra DB hosted on AWS.

Author: Alexander Arzt (ata122@ic.ac.uk)
Date: 19. Januar 2023

"""
import os
import random
import string
from multiprocessing import current_process
from cassandra.cluster import Cluster, DriverException
from cassandra.protocol import SyntaxException
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import website
from .users import User

MULTIPROCESS_SESSION = None


def establish_connection():
    """
    This function initializes the connection to the DB using
    the credentials supplied below.

    Args:
        None

    Returns:
        Return a instance of the Cluster class - which is an
        abstraction for the connection to the DB.

    """
    if os.environ.get('IN_DOCKER_CONTAINER', False):
        cloud_config = {'secure_connect_bundle':
                        './website/utilities/secure-connect-yapp-db.zip'}
    else:
        cloud_config = {'secure_connect_bundle':
                        ("/workspaces/new-on-youtube/server/website/"
                         "utilities/secure-connect-yapp-db.zip")}

    auth_provider = PlainTextAuthProvider('CiiWFpFfaQtfJtfOGBnpvazM',
                                          ("9oCeGIhPBE,.owYt.cp2mZ7S20Ge2_"
                                           "bLyL9oCRlqfZ5bcIR-Bz2mMd3tcA05PXx_"
                                           "TZ_JcoCYZpRyD0SSZsS.Zt02jvzUmLU9F0"
                                           "+iA+6HYd0mY5wd61D8vQv8q+_-eKGU"))
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster.connect()


def create_session():
    """Initialiases the global MULTIPROCESS_SESSION object, used
       by child processes to access the cassandra cluster, without
       needing to create mutliple instances.
    """

    global MULTIPROCESS_SESSION
    MULTIPROCESS_SESSION = establish_connection()
    MULTIPROCESS_SESSION.row_factory = dict_factory


def is_background_process():
    """Checks if current process is main or a background process
       responsible for batch processing.
    """

    if current_process().name in ["batch_1", "batch_2"]:
        return True
    return False


def query_users(username):
    """
    This function performs a query on the users DB based on either
    the username or user_id of a user and returns a User object if
    the user is present in the DB. Both username and user_id are
    possible arguments as both should be unique in the DB.

    Args:
        username (string): The username of user to the return

    Returns:
        User object

    Raises:
        HTTPException 500 if no valid search terms were passed as arguments
        or there are multiple users in the DB with the same username.
    """
    if not username:
        return None

    cql = "SELECT * FROM summaries.users WHERE username = %s"
    query = website.session.execute(cql, (username,))

    if query:
        query = query[0]
        topics = [x.strip() for x in
                  query['categories'].replace(';', ',').split(",")]
        channels = [x.strip() for x in
                    query['channels'].replace(';', ',').split(",")]
        watched_videos = query['three_watched']
        if watched_videos:
            watched_videos = query['three_watched'].split(":")
        else:
            watched_videos = ["", "", ""]
        userobj = User(query['id'],
                       query['username'],
                       query['password'],
                       topics,
                       watched_videos,
                       channels)
        return userobj
    return None


def insert_user(userobj):
    """
    This function performs an insertion into the users DB and returns True
    if the operation was successful - and false otherwise.

    Args:
        userobj (User object): User object with all user information to
        insert into DB except for id.

    Returns:
        Boolean

    """
    if not type(userobj) is User or \
       not userobj.username or \
       not userobj.password:
        return False
    try:
        topics = ','.join(userobj.topics)
        channels = ','.join(userobj.channels)
        watched_videos = ":".join(userobj.watched_videos)
        values = " VALUES (%s,%s,%s, UUID(),%s, %s)"
        prepend = """INSERT INTO summaries.users (username, categories,
                     channels, id, password, three_watched)"""
        website.session.execute(
            prepend+values, (userobj.username, topics, channels,
                             userobj.password, watched_videos))
    except DriverException as exception:
        print("DriverException: " + str(exception))
        return False
    return True


def set_user_topics(username, topics):
    """
    This function updates a users set of topics in the DB

    Args:
        userobj (User object): User object of the user to update
        topics [string]: List to topics to be updated in DB

    Returns:
        Boolean representing success of DB update operation
    """
    topics = ','.join(topics)
    cql = "UPDATE summaries.users SET categories = %s WHERE username = %s"
    try:
        website.session.execute(cql, (topics, username))
    except DriverException as exception:
        print("DriverException: " + str(exception))
        return False
    return True


def delete_database_entry(entry):
    """
    Deletes an entry from the database.

    Args:
        entry (dict[str, str]): metadata for an entry in the database

    Returns:
        bool: true if successful, false otherwise
    """

    keyword = entry["keyword"]
    views = entry["views"]
    likes = entry["likes"]
    video_name = entry["video_title"]
    channel_name = entry["channel_name"]
    video_id = entry["video_id"]

    cql = f"""DELETE from summaries.video_summaries where
             keyword='{keyword}' and views={views} and
             likes={likes} and video_title='{video_name}'
             and channel_name='{channel_name}' and video_id=
             '{video_id}'"""

    try:
        website.session.execute(cql)
        print(f"Deleted {video_name} from the database!", flush=True)
        return True
    except (DriverException, SyntaxException):
        return False


def query_random_videos(amount):
    """Queries a number of random videos from the database
       and returns them.

    Args:
        amount (int): number of videos to be retrieved

    Returns:
        list[dict[any]]: query response
    """

    try:
        cql = "SELECT * from summaries.video_summaries Limit " + str(amount)
        response = website.session.execute(cql)
        return response.all()
    except DriverException as exception:
        print("DriverException: " + str(exception))
        return None


def add_watched_video(username, video_id):
    """
    This function performs an update on the users DB and returns True
    if the operation was successful - and false otherwise. In the
    colon separated list of three most watched videos (most recent
    towards front of string) it pops off the oldest video and adds the
    new video_id to the front of the string.

    Args:
        username string: user to update
        video_id string: new video id to add as most recent video watched

    Returns:
        Boolean representing success of update operation

    """
    watched_videos = query_users(username).watched_videos
    if video_id in watched_videos:
        return True

    watched_videos = [video_id] + watched_videos[:2]
    watched_videos = ':'.join(watched_videos)

    cql = "UPDATE summaries.users SET three_watched = %s WHERE username = %s"
    try:
        website.session.execute(cql, (watched_videos, username))
    except DriverException as exception:
        print("DriverException: " + str(exception))
        return False
    print(f"Updated most recent watched videos for {username}: "
          f"{watched_videos.split(':')}", flush=True)
    website.recommender.train_model()
    return True


def add_videos_to_queue(topics):
    """
    This function adds a topic to the pubsub queue if there are
    to few videos in the DB for that topic

    Args:
        topics [string]: List to topics to check. Each topic is checked
        individually to ensure enough videos are present with that
        keyword in the DB

    Returns:
        void
    """
    topics = convert_topic_for_generalisation(topics)
    for topic in topics:
        cql = "SELECT * FROM summaries.video_summaries WHERE keyword = %s"
        response = website.session.execute(cql, (topic,)).all()
        if len(response) < 5:
            website.publisher.create_task(topic, str(5))


def add_more_videos_to_queue(topic, number):
    topic = convert_topic_for_generalisation([topic])[0]
    website.publisher.create_task(topic, str(number))


def db_contains_video(keyword, video_id):
    """
    This function checks if a video is already in our db so
    we don't have to summarize it all over again.

    Args:
        keyword (str): The keyword used to search the video.
        video_id (str): The unique video ID of the video from YT API
    Return:
        bool: True if video is in DB - False otherwise
    """
    cql = """SELECT video_id FROM summaries.video_summaries
            WHERE keyword = %s"""
    keyword = convert_topic_for_generalisation([keyword])[0]
    if is_background_process():
        response = MULTIPROCESS_SESSION.execute(cql, (keyword,)).all()
    else:
        response = website.session.execute(cql, (keyword,)).all()
    for video in response:
        if video['video_id'] == video_id:
            return True
    return False


def get_unique_topics():
    """
    This function retrieves all unique topics currently in the database
    Return:
        List[str]: list of unique topics in the database
    """
    cql = """SELECT keyword FROM summaries.video_summaries"""

    try:
        response = website.session.execute(cql).all()
    except DriverException as exception:
        print("Database Error:", exception)
        return []

    return sorted(list(set(map(lambda r:
                        convert_topic_for_readability(r["keyword"]),
                        response))))


def get_recommended_videos(username, amount):
    """
    This function performs a query on the DB and returns a list of
    dictionaries (keyword, likes, video_title, published_at, video_id,
    summary, views) - each belonging to one of the top 'amount' ranked
    YT videos which sorted by 'sort_by'

    Args:
        topics [string]: The topics of which to return
        amount int: The number of videos to return
        sort_by str: The method with which to sort the result

    Returns:
        [dict]

    """
    amount = int(amount)
    recommended_video_ids = website.recommender.recommend_videos_for_user(
        username, amount)
    if not recommended_video_ids:
        return []
    cql = """SELECT keyword, likes, video_title, published_at, video_id,
             summary, views, channel_name FROM summaries.video_summaries
             WHERE video_id IN ("""
    cql += ','.join(['%s'] * len(recommended_video_ids))
    cql += ") ALLOW FILTERING;"
    params = tuple(recommended_video_ids)

    try:
        response = website.session.execute(cql, params).all()
        response_unique = []
        added_video_ids = set()
        for video in response:
            if video['video_id'] not in added_video_ids:
                added_video_ids.add(video['video_id'])
                response_unique.append(video)

    except DriverException as exception:
        print("Exception when querying DB: " + str(exception))
        return []
    random.shuffle(response_unique)
    return response_unique


def query_videos(topics, amount, sort_by):
    """
    This function performs a query on the DB and returns a list of
    dictionaries (keyword, likes, video_title, published_at, video_id,
    summary, views) - each belonging to one of the top 'amount' ranked
    YT videos which sorted by 'sort_by'

    Args:
        topics [string]: The topics of which to return
        amount int: The number of videos to return
        sort_by str: The method with which to sort the result

    Returns:
        [dict]

    """
    amount = int(amount)
    topics = convert_topic_for_generalisation(topics)
    cql = """SELECT keyword, likes, video_title, published_at, video_id,
             summary, views, channel_name FROM summaries.video_summaries
             WHERE keyword IN ("""
    cql += ','.join(['%s'] * len(topics))
    cql += ")"
    params = tuple(topics)

    try:
        response = website.session.execute(cql, params).all()
    except DriverException as exception:
        print("Exception when querying DB: " + str(exception))
        return []

    if sort_by == 'Popular':
        response = sorted(response, key=lambda x: x['views'], reverse=True)
    elif sort_by == 'Liked':
        response = sorted(response, key=lambda x: x['likes'], reverse=True)
    elif sort_by == 'Recent':
        response = sorted(
            response, key=lambda x: x['published_at'], reverse=True)
    else:
        random.shuffle(response)
    if len(response) < amount:
        add_videos_to_queue(topics)
    return response[:amount]


def insert_video(video_dict):
    """
    This function performs an insertion into the DB and returns True
    if the operation was successful - and false otherwise.

    Args:
        video_dict (dict): A dictionary containing the keys:
                           {'keyword','video_title', 'channel_name',
                           'summary'} and the correspoding values must
                           all be of type string.

    Returns:
        Boolean

    """

    keyword = convert_topic_for_generalisation([video_dict["keyword"]])[0]
    views = video_dict["views"]
    likes = video_dict["likes"]
    video_name = video_dict["video_name"]
    channel_name = video_dict["channel_name"]
    video_id = video_dict["video_id"]
    published_at = video_dict["published_at"]
    summary = clean_summary(video_dict["summary"])
    vid_tags = ','.join(video_dict["video_tags"])

    params = [keyword, views, likes, video_name, channel_name, video_id,
              published_at, summary, vid_tags]

    cql = """INSERT INTO summaries.video_summaries (keyword,
                 views, likes, video_title, channel_name, video_id,
                 published_at, summary, video_tags) VALUES ("""
    cql += ','.join(['%s'] * len(params))
    cql += ");"

    params = tuple(params)

    try:
        if is_background_process():
            MULTIPROCESS_SESSION.execute(cql, params)
        else:
            website.session.execute(cql, params)
        print("Insertion successful --------- ", flush=True)
        print("Keyword: " + keyword + " | Video Title: " + video_name +
              " | Channel : " + channel_name + "\n", flush=True)
    except DriverException as exception:
        print(str(exception))
        print("Insertion Failed ! ----------- ", flush=True)
        print("Keyword: " + keyword + " | Video Title: " + video_name +
              " | Channel : " + channel_name + "\n", flush=True)
        return False
    return True


def query_all_videos():
    """
    This function performs a query on the DB and returns a list of
    dictionaries (video_title, video_id, summary, video_tags from
    summaries.video_summaries)

    Returns:
        [dict]

    """

    cql = """select video_title, video_id, summary, video_tags from
             summaries.video_summaries"""
    query = website.session.execute(cql).all()
    return query


def convert_topic_for_generalisation(topics):
    return [topic.lower().replace(" ", "_") for topic in topics]


def convert_topic_for_readability(topic):
    topic = topic.replace("_", " ")
    topic = string.capwords(topic)
    return topic


def clean_summary(summary):
    if summary[:15] == "This transcript":
        summary = "This video" + summary[15:]
    elif summary[:18] == "In this transcript":
        summary = "This video" + summary[18:]
    return summary
