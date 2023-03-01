"""
This file contains all functions related to database operations for the
applications Apache Cassandra DB hosted on AWS.

Author: Alexander Arzt (ata122@ic.ac.uk)
Date: 19. Januar 2023

"""
import os
import random
from cassandra.cluster import Cluster, DriverException
from cassandra.auth import PlainTextAuthProvider
import website
from .users import User
from .publisher import Publisher


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
    watched_videos = [video_id] + watched_videos[:2]
    watched_videos = ':'.join(watched_videos)

    cql = "UPDATE summaries.users SET three_watched = %s WHERE username = %s"
    try:
        website.session.execute(cql, (watched_videos, username))
    except DriverException as exception:
        print("DriverException: " + str(exception))
        return False
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
    topics = clean_topics(topics)
    publisher = Publisher()
    for topic in topics:
        cql = "SELECT * FROM summaries.video_summaries WHERE keyword = %s"
        response = website.session.execute(cql, (topic,)).all()
        if len(response) < 5:
            publisher.create_task(topic, str(5))


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
    keyword = clean_topics([keyword])[0]
    response = website.session.execute(cql, (keyword,)).all()
    for video in response:
        if video['video_id'] == video_id:
            return True
    return False


def query_videos(topics, amount, sort_by, username=None):
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
    topics = clean_topics(topics)
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

    if sort_by == 'Recommended':
        # TO BE IMPLEMENTED - call recommender function here
        pass
    elif sort_by == 'Popular':
        response = sorted(response, key=lambda x: x['views'], reverse=True)
    elif sort_by == 'Recent':
        # TO BE IMPLEMENTED
        pass
    elif sort_by == 'Random':
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

    keyword = clean_topics([video_dict["keyword"]])[0]
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
    cql += ")"

    params = tuple()

    try:
        website.session.execute(cql, params)
        print("Insertion successful --------- ")
        print("Keyword: " + keyword + " | Video Title: " + video_name +
              " | Channel : " + channel_name + "\n")
    except DriverException as exception:
        print(str(exception))
        print("Insertion Failed ! ----------- ")
        print("Keyword: " + keyword + " | Video Title: " + video_name +
              " | Channel : " + channel_name + "\n")
        return False
    return True


def clean_topics(topics):
    return [topic.lower().replace(" ", "_") for topic in topics]


def clean_summary(summary):
    if summary[:15] == "This transcript":
        summary = "This video" + summary[15:]
    return summary
