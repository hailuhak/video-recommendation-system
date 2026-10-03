import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load YouTube videos
videos = pd.read_csv("data/youtube_videos.csv")


# Combine title and description
videos["text"] = (
    videos["title"].fillna("")
    + " "
    + videos["description"].fillna("")
)


# Convert text into TF-IDF vectors
vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(videos["text"])


print("Number of videos:", len(videos))
print("Number of features:", len(vectorizer.get_feature_names_out()))
print("TF-IDF matrix shape:", tfidf_matrix.shape)


# Calculate similarity between all videos
similarity_matrix = cosine_similarity(tfidf_matrix)


print("\nSimilarity matrix:")
print(similarity_matrix)