import pandas as pd
import os
import numpy as np
from cassandra.cluster import Cluster, DriverException
from cassandra.auth import PlainTextAuthProvider
from sklearn.feature_extraction.text import TfidfVectorizer
import random
from sklearn.metrics.pairwise import sigmoid_kernel
import website


class QueryFailedException(Exception):
    pass


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
        query = website.session.execute(
            "select video_title, video_id, summary, video_tags from summaries.video_summaries").all()
        if not query:
            raise QueryFailedException(
                "Could not retrieve all videos from database.")
        return query

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
        print("Recommender model trained")

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
            self.video_df.index, index=self.video_df["video_id"])

    def give_recommendation(self, vid_id, k, title=False):
        """
        Main function which lets the trained model generate predictions.

        Args:
            - vid_id (string): The ID of the video for which we want to generate recommendations
            - k (int): The top k most similar videos compared to the video with vid_ID.
            - title (bool): If true then video titles are returned instead of video IDs.
        """
        idx = self.indices[vid_id]
        if idx.size == 2:
            idx = idx[1]

        # get pairwise similarity scores
        sig_scores = list(enumerate(self.sigmoid_scores[idx]))
        # sort
        # print(sig_scores)
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
        # get top 10 most similar videos
        sig_scores = sig_scores[1:k]
        # get vid idxs
        vid_idx = [i[0] for i in sig_scores]
        if title:
            return list(self.video_df["video_title"].iloc[vid_idx])
        else:
            return list(self.video_df["video_id"].iloc[vid_idx])

    def recommend_videos_for_user(self, username, amount, shuffle=True):
        """
        Main function which lets the trained model generate predictions for a specific user.

        Args:
            - username (string): The username of the user for whom we want to generate recommendations for.
            - shuffle (bool): If True (default) then the results are returned in random order.
        Returns:
            list[str]: The video IDs of the recommended videos.
        """

        query = website.session.execute(
            f"select three_watched from summaries.users where username='{username}';").all()

        if not query:
            raise QueryFailedException(
                f"Could not retrieve three_watched field for user {username}.")

        results = []
        three_watched = query[0]['three_watched'].split(":")
        three_watched = [x for x in three_watched if x]

        if len(three_watched) == 3:
            amount_weighting = [0.6, 0.25, 0.15]
            amount_1 = int(amount * amount_weighting[0])
            amount_2 = int(amount * amount_weighting[1])
            amount_3 = amount - amount_1 - amount_2
            amounts = [amount_1, amount_2, amount_3]
        elif len(three_watched) == 2:
            amount_weighting = [0.7, 0.3]
            amount_1 = int(amount * amount_weighting[0])
            amount_2 = amount - amount_1
            amounts = [amount_1, amount_2]
        elif len(three_watched) == 1:
            amounts = [amount]
        else:
            return None

        for vid_id, k in zip(three_watched, amounts):
            results.append(self.give_recommendation(vid_id, k, title=False))

        flattened_results = [item for sublist in results for item in sublist]
        if shuffle:
            random.shuffle(flattened_results)

        return flattened_results
