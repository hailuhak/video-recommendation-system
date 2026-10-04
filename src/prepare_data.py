import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load YouTube dataset
videos = pd.read_csv(
    "data/youtube_videos.csv"
)


# Handle missing descriptions
videos["description"] = (
    videos["description"]
    .fillna("")
)


# Combine title and description
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


# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    min_df=2,
    max_df=0.90,
)

# Convert text into numerical vectors
tfidf_matrix = vectorizer.fit_transform(
    videos["text"]
)


# Calculate similarity between all videos
similarity_matrix = cosine_similarity(
    tfidf_matrix
)


print("Dataset shape:")
print(videos.shape)


print("\nTF-IDF matrix shape:")
print(tfidf_matrix.shape)


print("\nNumber of features:")
print(
    len(
        vectorizer.get_feature_names_out()
    )
)


print("\nSimilarity matrix shape:")
print(
    similarity_matrix.shape
)


print(
    "\nSimilarity between first video and itself:"
)

print(
    similarity_matrix[0][0]
)


# Recommendation function
def recommend_videos(
    video_index,
    number_of_recommendations=5,
):

    similarities = similarity_matrix[
        video_index
    ]

    similar_indices = (
        similarities
        .argsort()[::-1]
    )

    recommended_indices = (
        similar_indices[
            1:number_of_recommendations + 1
        ]
    )

    recommendations = videos.iloc[
        recommended_indices
    ].copy()

    # Add similarity scores
    recommendations["similarity"] = (
        similarities[recommended_indices]
    )

    return recommendations


# Test recommendations
print(
    "\nRecommendations for first video:"
)

recommendations = recommend_videos(
    video_index=0,
    number_of_recommendations=5,
)


for _, video in recommendations.iterrows():

    print(
        f"- {video['title']}"
    )

    print(
        f"  Similarity: "
        f"{video['similarity']:.3f}"
    )