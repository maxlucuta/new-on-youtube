import pandas as pd
import os
import numpy as np
from cassandra.cluster import Cluster, DriverException
from cassandra.auth import PlainTextAuthProvider
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


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


global session
session = establish_connection()


class Recommender:

    def __init__(self):
        self.sparse_matrix = None
        self.indices = None
        self.sigmoid_scores = None
        self.video_df = None
        self.tfv = TfidfVectorizer(max_df=0.3, max_features=None, strip_accents="ascii",
                                   analyzer="word", token_pattern=u'(?ui)\\b\\w*[a-z]+\\w*\\b',
                                   ngram_range=(1, 1), stop_words="english")

    def _query_all_videos(self):
        """
        This function performs a query on the DB and returns a list of  
        dictionaries (video_title, video_id, summary, video_tags from summaries.video_summaries)

        Returns:
            [dict]

        """
        query = session.execute(
            "select video_title, video_id, summary, video_tags from summaries.video_summaries").all()
        if query:
            result = [{'video_title': x.video_title, 'ID': x.video_id,
                       'summary': x.summary, "video_tags": x.video_tags} for x in query]
            return result
        else:
            return [{"ERROR": "Query failed"}]

    def _clean_data(self, dicts):
        """
        Helper function that cleans the data and joins video_tags, video_title, 
        and summary into one string.

        Args:
            None
        Return Type:
            None
        """
        vids = pd.DataFrame(dicts)
        vids["video_tags"] = vids["video_tags"].apply(
            lambda x: x.replace(",", " "))
        vids["summary"] = vids["video_title"] + " " + \
            vids["video_tags"] + " " + vids["summary"]
        vids["summary"] = vids["summary"].fillna(" ")
        self.video_df = vids

    def _calc_sparse_matrix(self):
        """
        Helper function which computes the feature matrix.

        Args:
            None
        Return Type:
            None
        """

        matrix = self.tfv.fit_transform(self.video_df["summary"])
        self.sparse_matrix = matrix

    def _calc_sigmoid_scores(self):
        """
        Helper function pairwise similiarity score matrix.

        Args:
            None
        Return Type:
            None
        """
        self.sigmoid_scores = sigmoid_kernel(
            self.sparse_matrix, self.sparse_matrix)

    def train_model(self):
        """
        Core function which runs the entire pipeline 
        from fetching the data, cleaning it and then 
        calculating the required matrices.

        Args:
            None
        Return Type:
            None
        """

        raw_videos = self._query_all_videos()
        self._clean_data(raw_videos)
        self._reverse_mapper()
        self._calc_sparse_matrix()
        self._calc_sigmoid_scores()

    def _reverse_mapper(self):
        """
        Helper function which maps numerical index of
        the videos to video_idx.

        Args:
            None
        Return Type:
            None
        """
        self.indices = pd.Series(
            self.video_df.index, index=self.video_df["ID"])

    def give_recommendation(self, vid_id, k, title=False):
        """
        Main function which lets the trained model generate predictions.

        Args:
            - vid_id (string): The ID of the video for which we want to generate recommendations
            - k (int): The top k most similar videos compared to the video with vid_ID.
            - title (bool): If true then video titles are returned instead of video IDs. 
        """
        idx = self.indices[vid_id]
        # get pairwise similarity scores
        sig_scores = list(enumerate(self.sigmoid_scores[idx]))
        # sort
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
        # get top 10 most similar videos
        sig_scores = sig_scores[1:k]
        # get vid idxs
        vid_idx = [i[0] for i in sig_scores]
        if title:
            return self.video_df["video_title"].iloc[vid_idx]
        else:
            return self.video_df["ID"].iloc[vid_idx]


if __name__ == "__main__":
    rec = Recommender()
    rec.train_model()
    print("-------------- Test Recommendations ------------------")
    print("\n For a gaming video: ")
    print(rec.give_recommendation("L5kff6EUKwI", 10, True))

    print("\n For a football video: ")
    print(rec.give_recommendation("KmZ3x_7D1wE", 10, True))

    print("\n For a reality tv video: ")
    print(rec.give_recommendation("5Bx0w0K8_BE", 10, True))

    print("\n For a economic news video: ")
    print(rec.give_recommendation("-M_3yJPgGxU", 10, True))
