"""
The purpose of this script is to run it from the command line
and fill up the DB with the k most popular videos that came up
when searching for videos using <keyword>

Author: Alexander Arzt
Date: 8. Februar, 2023
"""


import sys

# from threading import Thread
# from website.utilities.subscriber import process_tasks
# from website.utilities.database import query_yt_videos


from website.utilities.youtube import (
    get_most_popular_video_transcripts_by_topic
)

from website.utilities.database import establish_connection, insert_into_DB
import googleapiclient.errors as googleapi_errors

try:
    conn = establish_connection()
    res = get_most_popular_video_transcripts_by_topic(
        sys.argv[1], int(sys.argv[2]))

    for i in res:
        ins = insert_into_DB(i, conn)


except googleapi_errors.HttpError as err:
    if err.resp.status == 403:
        print("Warning: Daily YouTube API quota exceeded.")
