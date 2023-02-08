"""
This file contains all functions related to database operations for the
applications Apache Cassandra DB hosted on AWS.

Author: Alexander Arzt (ata122@ic.ac.uk)
Date: 19. Januar 2023

"""
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from flask import abort
from uuid import UUID
from .users import User


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
                        '/website/utilities/secure-connect-yapp-db.zip'}
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
    session = cluster.connect()
    return session


def query_yt_videos(keyword, k, session):
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
    query = session.execute(
        f"""select * from summaries.video_summaries where
            keyword = '{keyword}' limit {k}""").all()
    if query:
        result = [{'video_title': x.video_title,
                   'channel_name': x.channel_name,
                   'summary': x.summary} for x in query]
        return result
    else:
        # create_task(keyword, str(k))
        return [{"ERROR": "Query failed"}]


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


def insert_into_DB(video_dict, session):
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
    summary = string_cleaner(video_dict["summary"])
    keyword = string_cleaner(video_dict["keyword"])
    video_name = string_cleaner(video_dict["video_name"])
    channel_name = string_cleaner(video_dict["channel_name"])

    values = f""" VALUES ('{keyword}',
                          '{video_name}',
                          '{channel_name}',
                          '{summary}',
                          '{vid_tags}',
                          {int(video_dict["views"])},
                          {int(video_dict["likes"])},
                          '{video_dict["published_at"]}')"""
    prepend = """INSERT INTO summaries.video_summaries (keyword,
                 video_title, channel_name, summary, video_tags, views,
                 likes, published_at)"""

    try:
        # result = session.execute(prepend+values)
        # Need to use result for error handling
        session.execute(prepend+values)
        return True
    except Exception:
        return False


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

    session = establish_connection()
    # Need to update this to first check for global session
    # Same for functions higher up

    if username:
        query = session.execute(f"""select * from summaries.users
                                    where username = '{username}'""").all()
    else:
        try:
            UUID(str(user_id))
        except ValueError:
            return None
        query = session.execute(f"""select * from summaries.users where
                                 id = {user_id} allow filtering""").all()

    if len(query) > 1:
        abort(500)

    if query:
        query = query[0]
        categories = [x.strip() for x in
                      query.categories.replace(';', ',').split(",")]
        channels = [x.strip() for x in
                    query.channels.replace(';', ',').split(",")]
        userobj = User(query.id,
                       query.username,
                       query.password,
                       categories,
                       channels)
        return userobj
    else:
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
        session = establish_connection()
        # Need to update the above to first check for global session
        # Same for functions higher up
        categories = ','.join(userobj.categories)
        channels = ','.join(userobj.channels)
        values = f""" VALUES ('{userobj.username}',
                      '{categories}','{channels}',
                      UUID(),'{userobj.password}')"""
        prepend = """INSERT INTO summaries.users
                     (username, categories, channels, id, password)"""
        # result = session.execute(prepend+values)
        # Need to use result for error handling
        session.execute(prepend+values)
        return True
    except Exception:
        return False
