# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

import os
from dotenv import load_dotenv

load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")

print("YouTube API key loaded:", bool(youtube_api_key))
# videos = pd.read_csv("data/videos.csv")
# interactions = pd.read_csv("data/interactions.csv")

# print("Videos:")
# print(videos)

# print("\nInteractions:")
# print(interactions)

# print("\nVideo dataset shape:")
# print(videos.shape)

# print("\nInteraction dataset shape:")
# print(interactions.shape)

# print("\nVideo categories:")
# print(videos["category"].value_counts())

# user_1 = interactions[interactions["user_id"] == 1]

# print("\nUser 1 interactions:")
# print(user_1)

# liked_by_user_1 = user_1[user_1["liked"] == 1]

# print("\nVideos liked by User 1:")
# print(liked_by_user_1)

# user_1_videos = user_1.merge(videos, on="video_id")

# print("\nUser 1 videos:")
# print(user_1_videos)

# watched_video_ids = user_1["video_id"]

# unwatched_videos = videos[
#     ~videos["video_id"].isin(watched_video_ids)
# ]

# print("\nVideos User 1 has not watched:")
# print(unwatched_videos)

# video_popularity = (
#     interactions.groupby("video_id")
#     .agg(
#         total_views=("video_id", "count"),
#         total_likes=("liked", "sum"),
#     )
#     .reset_index()
# )

# print("\nVideo popularity:")
# print(video_popularity)


# video_popularity = video_popularity.sort_values(
#     by="total_likes",
#     ascending=False
# )

# print("\nVideos ranked by popularity:")
# print(video_popularity)

# popular_videos = video_popularity.merge(
#     videos,
#     on="video_id"
# )

# print("\nPopular videos:")
# print(popular_videos)

# recommendations = popular_videos[
#     ~popular_videos["video_id"].isin(watched_video_ids)
# ]

# print("\nRecommendations for User 1:")
# print(recommendations)

# liked_videos = user_1_videos[user_1_videos["liked"] == 1]

# print("\nVideos liked by User 1:")
# print(liked_videos)
# liked_categories = liked_videos["category"].unique()

# print("\nCategories User 1 likes:")
# print(liked_categories)
# content_recommendations = unwatched_videos[
#     unwatched_videos["category"].isin(liked_categories)
# ]

# print("\nContent-based recommendations:")
# print(content_recommendations)

# titles = videos["title"]

# print("\nVideo titles:")
# print(titles)

# video_text = (
#     videos["title"] + " " + videos["category"]
# )

# vectorizer = TfidfVectorizer()

# tfidf_matrix = vectorizer.fit_transform(video_text)
# similarity_matrix = cosine_similarity(tfidf_matrix)

# print("\nSimilarity matrix shape:")
# print(similarity_matrix.shape)

# print("\nSimilarity to Video 1:")
# print(similarity_matrix[0])

# def recommend_similar_videos(video_id, top_n=3):
#     video_index = videos.index[
#         videos["video_id"] == video_id
#     ][0]

#     similarity_scores = similarity_matrix[video_index]

#     similar_video_indices = similarity_scores.argsort()[::-1]

#     similar_video_indices = similar_video_indices[1:top_n + 1]

#     recommendations = videos.iloc[similar_video_indices]

#     return recommendations

# print("\nVideos similar to Python for Beginners:")

# print(
#     recommend_similar_videos(1)
# )

# video_text = (
#     videos["title"] + " " + videos["category"]
# )

# print("\nVideo text:")
# print(video_text)

# print("\nVideos similar to Python for Beginners:")

# print(
#     recommend_similar_videos(1)
# )