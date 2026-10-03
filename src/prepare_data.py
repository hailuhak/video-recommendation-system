import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


videos = pd.read_csv("data/youtube_videos.csv")


videos["text"] = (
    videos["title"].fillna("")
    + " "
    + videos["description"].fillna("")
)


vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(videos["text"])


similarity_matrix = cosine_similarity(tfidf_matrix)


print("Number of videos:", len(videos))

print(
    "Number of features:",
    len(vectorizer.get_feature_names_out()),
)

print("TF-IDF matrix shape:", tfidf_matrix.shape)


def recommend_videos(video_index, number_of_recommendations=3):
    similarities = similarity_matrix[video_index]

    similar_indices = similarities.argsort()[::-1]

    recommended_indices = similar_indices[
        1:number_of_recommendations + 1
    ]

    return videos.iloc[recommended_indices]


print("\nRecommendations:")

recommendations = recommend_videos(0)

for _, video in recommendations.iterrows():
    print(video["title"])