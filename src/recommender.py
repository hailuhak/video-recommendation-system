import pandas as pd

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


def create_similarity_matrix(
    videos
):

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

    similarity_matrix = (
        cosine_similarity(
            tfidf_matrix
        )
    )

    return similarity_matrix


def recommend_videos(
    videos,
    similarity_matrix,
    video_id,
    number_of_recommendations=5,
):

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