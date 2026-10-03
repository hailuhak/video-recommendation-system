
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_videos(filename="data/youtube_videos.csv"):

    videos = pd.read_csv(filename)

    videos["text"] = (
        videos["title"].fillna("")
        + " "
        + videos["description"].fillna("")
    )

    return videos


def create_similarity_matrix(videos):

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        videos["text"]
    )

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    return similarity_matrix


def recommend_videos(
    videos,
    similarity_matrix,
    video_id,
    number_of_recommendations=3,
):

    video_index = videos.index[
        videos["video_id"] == video_id
    ].tolist()

    if not video_index:
        return pd.DataFrame()

    video_index = video_index[0]

    similarities = similarity_matrix[video_index]

    similar_indices = similarities.argsort()[::-1]

    recommended_indices = [
        index
        for index in similar_indices
        if index != video_index
    ][:number_of_recommendations]

    return videos.iloc[recommended_indices]
