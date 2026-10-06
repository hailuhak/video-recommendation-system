
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_videos(
    filename="data/youtube_videos.csv"
):
    videos = pd.read_csv(
        filename
    )

    # Handle missing descriptions
    videos["description"] = (
        videos["description"]
        .fillna("")
    )

    # Give title more importance
    videos["text"] = (
        videos["title"]
        + " "
        + videos["title"]
        + " "
        + videos["title"]
        + " "
        + videos["description"]
    )

    # Convert text to lowercase
    videos["text"] = (
        videos["text"]
        .str.lower()
    )

    return videos


def create_tfidf_model(videos):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        min_df=2,
        max_df=0.90,
    )

    tfidf_matrix = (
        vectorizer.fit_transform(
            videos["text"]
        )
    )

    return vectorizer, tfidf_matrix


def create_similarity_matrix(
    tfidf_matrix
):

    similarity_matrix = (
        cosine_similarity(
            tfidf_matrix
        )
    )

    return similarity_matrix


def create_user_profile(
    videos,
    interactions,
    tfidf_matrix,
):
    """
    Create a user profile from videos
    the user has watched.
    """

    watched_video_ids = interactions[
        interactions["event_type"] == "view"
    ]["video_id"].tolist()

    watched_indices = videos.index[
        videos["video_id"].isin(
            watched_video_ids
        )
    ].tolist()

    if not watched_indices:
        return None

    watched_vectors = tfidf_matrix[
        watched_indices
    ]

    user_profile = watched_vectors.mean(
        axis=0
    )

    return np.asarray(
        user_profile
    )


def recommend_for_user(
    videos,
    interactions,
    tfidf_matrix,
    user_profile,
    number_of_recommendations=5,
):
    """
    Recommend unseen videos based on
    the user's watch history.
    """

    if user_profile is None:
        return pd.DataFrame()

    # Calculate similarity between
    # user profile and every video
    user_similarities = cosine_similarity(
        user_profile,
        tfidf_matrix,
    ).flatten()

    # Find videos the user has already watched
    watched_video_ids = set(
        interactions[
            interactions["event_type"] == "view"
        ]["video_id"]
    )

    # Create a copy so we don't modify
    # the original dataset
    recommendations = videos.copy()

    # Add recommendation score
    recommendations["score"] = (
        user_similarities
    )

    # Remove videos already watched
    recommendations = recommendations[
        ~recommendations["video_id"].isin(
            watched_video_ids
        )
    ]

    # Sort from highest score to lowest
    recommendations = recommendations.sort_values(
        "score",
        ascending=False,
    )

    # Return the top recommendations
    return recommendations.head(
        number_of_recommendations
    )


def recommend_videos(
    videos,
    similarity_matrix,
    video_id,
    number_of_recommendations=5,
):
    """
    Recommend videos similar to a given video.
    """

    video_index = videos.index[
        videos["video_id"] == video_id
    ].tolist()

    if not video_index:
        return pd.DataFrame()

    video_index = video_index[0]

    similarities = (
        similarity_matrix[
            video_index
        ]
    )

    similar_indices = (
        similarities
        .argsort()[::-1]
    )

    recommended_indices = [
        index
        for index in similar_indices
        if index != video_index
    ][
        :number_of_recommendations
    ]

    recommendations = (
        videos.iloc[
            recommended_indices
        ].copy()
    )

    recommendations["similarity"] = (
        similarities[
            recommended_indices
        ]
    )

    return recommendations


def precision_at_k(
    recommendations,
    liked_video_ids,
    k=5,
):
    """
    Calculate Precision@K.

    Precision@K =
    relevant recommendations / K
    """

    top_recommendations = (
        recommendations.head(k)
    )

    recommended_video_ids = set(
        top_recommendations["video_id"]
    )

    liked_video_ids = set(
        liked_video_ids
    )

    relevant_recommendations = (
        recommended_video_ids
        & liked_video_ids
    )

    precision = (
        len(relevant_recommendations)
        / k
    )

    return precision
