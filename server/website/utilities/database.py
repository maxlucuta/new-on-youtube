"""
This file contains all functions related to database operations for the
applications Apache Cassandra DB hosted on AWS.

Author: Alexander Arzt (ata122@ic.ac.uk)
Date: 19. Januar 2023

"""
import os
from cassandra.cluster import Cluster, DriverException
from cassandra.auth import PlainTextAuthProvider
from uuid import UUID
from .users import User
from .publisher import Publisher
import website


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
    s = cluster.connect()
    return s


def query_yt_videos(keyword, k):
    """
    This function performs a query on the DB and returns a list of
    dictionaries (video_title, channel_name, summary) - each belonging
    to one of the top k-ranked YT videos.

    Args:
        keyword (string): The keyword which is used to tag the videos
        k (int): The first k ranked videos.
        session (cassandra.cluster.Cluster): The connection object to the DB

    Returns:
        [dict]

    """
    publisher = Publisher()
    try:
        query = website.session.execute(
            f"""select * from summaries.video_summaries where
                keyword = '{keyword}' limit {k}""").all()
    except DriverException:
        return []
    else:
        if len(query) > 0:
            result = [{
                'video_title': x.video_title,
                'channel_name': x.channel_name,
                'summary': x.summary,
                'video_id': x.video_id} for x in query]
            return result
        else:
            publisher.create_task(keyword, str(k))
            return []
            # the below exception should probably be
            # handled in the try-except statement
            # return [{"ERROR": "Query failed"}]


def check_if_video_is_already_in_DB(keyword, video_id):
    """
    This function checks if a video is already in our DB so
    we don't have to summarize it all over again.

    Args:
        keyword (str): The keyword used to search the video.
        video_id (str): The unique video ID of the video from YT API
        session (cassandra.cluster.Cluster): The connection object to the DB
    Return:
        bool: True if video is in DB - False otherwise
    """
    query = website.session.execute(
        f"""select video_id from summaries.video_summaries
         where keyword = '{keyword}';""")
    if query:
        result = [x.video_id for x in query]
        return result[0] == video_id
    else:
        return False


def string_cleaner(input_string):
    """
    This is a helper function which removes
    quotation marks from a string in order to avoid
    failure of DB insertion attempts.

    Args:
        input_string (str): The string to be cleaned.

    Returns:
        str: The cleaned string.
    """
    return input_string.replace("'", "").replace('"', '')


def insert_into_DB(video_dict):
    """
    This function performs an insertion into the DB and returns True
    if the operation was successful - and false otherwise.

    Args:
        video_dict (dict): A dictionary containing the keys:
                           {'keyword','video_title', 'channel_name',
                           'summary'} and the correspoding values must
                           all be of type string.

        session (cassandra.cluster.Cluster): The connection object to the DB

    Returns:
        Boolean

    """
    vid_tags = ','.join(video_dict["video_tags"])
    vid_tags = string_cleaner(vid_tags)
    summary = string_cleaner(video_dict["summary"])
    keyword = string_cleaner(video_dict["keyword"])
    video_name = string_cleaner(video_dict["video_name"])
    channel_name = string_cleaner(video_dict["channel_name"])
    video_id = video_dict["video_id"]

    values = f""" VALUES ('{keyword}',
                          {video_dict["views"]},
                          {video_dict["likes"]},
                          '{video_name}',
                          '{channel_name}',
                          '{video_id}',
                          '{video_dict["published_at"]}',
                          '{summary}',
                          '{vid_tags}')"""

    prepend = """INSERT INTO summaries.video_summaries (keyword,
                 views, likes, video_title, channel_name, video_id,
                 published_at, summary, video_tags)"""

    try:
        website.session.execute(prepend+values)
        print("Insertion successful --------- ")
        print("Keyword: " + keyword + " | Video Title: " + video_name +
              " | Channel : " + channel_name + "\n")
    except Exception:
        print(Exception)
        print("Insertion Failed ! ----------- ")
        print("Keyword: " + keyword + " | Video Title: " + video_name +
              " | Channel : " + channel_name + "\n")
        return False
    return True


def query_users_db(username=None, user_id=None):
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
    if not username and not user_id:
        return None

    if username:
        query = website.session.execute(f"""select * from summaries.users
                                    where username = '{username}'""").all()
    else:
        try:
            UUID(str(user_id))
        except ValueError:
            return None
        query = website.session.execute(f"""select * from summaries.users where
                                 id = {user_id} allow filtering""").all()

    if query:
        query = query[0]
        topics = [x.strip() for x in
                  query.categories.replace(';', ',').split(",")]
        channels = [x.strip() for x in
                    query.channels.replace(';', ',').split(",")]
        userobj = User(query.id,
                       query.username,
                       query.password,
                       topics,
                       channels)
        return userobj
    return None


def insert_user_into_db(userobj):
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
        values = f""" VALUES ('{userobj.username}',
                      '{topics}','{channels}',
                      UUID(),'{userobj.password}')"""
        prepend = """INSERT INTO summaries.users
                     (username, categories, channels, id, password)"""
        website.session.execute(prepend+values)
    except Exception:
        return False
    return True


def update_user_topics_in_db(username, topics):
    topics = ','.join(topics)
    values = f"""UPDATE summaries.users
                 SET categories = '{topics}'
                 WHERE username = '{username}'"""
    try:
        website.session.execute(values)
    except Exception:
        return False
    return True
