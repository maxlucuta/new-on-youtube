
from website.utilities.youtube import (
    get_most_popular_video_transcripts_by_topic
)

from website.utilities.database import establish_connection, insert_into_DB
import googleapiclient.errors as googleapi_errors

try:
    conn = establish_connection()
    res = get_most_popular_video_transcripts_by_topic("marble", 1)

    for i in res:
        ins = insert_into_DB(i, conn)
        print(ins)

except googleapi_errors.HttpError as err:
    if err.resp.status == 403:
        print("Warning: Daily YouTube API quota exceeded.")
