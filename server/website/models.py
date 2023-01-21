"""
This file contains all functions related to database operations for the 
applications Apache Cassandra DB hosted on AWS.

Author: Alexander Arzt (ata122@ic.ac.uk)
Date: 19. Januar 2023

"""

#necessary libraries for Apache Cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider



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
    cloud_config= {'secure_connect_bundle': '../secure-connect-yapp-db.zip'}
    auth_provider = PlainTextAuthProvider('CiiWFpFfaQtfJtfOGBnpvazM', 
                                          '9oCeGIhPBE,.owYt.cp2mZ7S20Ge2_bLyL9oCRlqfZ5bcIR-Bz2mMd3tcA05PXx_TZ_JcoCYZpRyD0SSZsS.Zt02jvzUmLU9F0+iA+6HYd0mY5wd61D8vQv8q+_-eKGU')
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
    query = session.execute(f"select * from summaries.video_summaries where keyword = '{keyword}' limit {k}").all()
    if query:
        result = [{'video_title': x.video_title, 'channel_name': x.channel_name, 'summary': x.summary} for x in query]
        return result
    else:
        return [{"ERROR": "Query failed"}]



def insert_into_DB(video_dict, session):
    """
    This function performs an insertion into the DB and returns True
    if the operation was successful - and false otherwise.   

    Args:
        video_dict (dict): A dictionary containing the keys: {'keyword','video_title', 'channel_name', 'summary'}
                           and the correspoding values must all be of type string. 

        session (cassandra.cluster.Cluster): The connection object to the DB

    Returns:
        Boolean

    """   
    try: 
        values = f""" VALUES ('{video_dict["keyword"]}', '{video_dict["video_title"]}', '{video_dict["channel_name"]}', '{video_dict["summary"]}')"""
        prepend = "INSERT INTO summaries.video_summaries (keyword, video_title, channel_name, summary)"
        result = session.execute(prepend+values)
        return True
    except: 
        return False


