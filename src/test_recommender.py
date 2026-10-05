import pandas as pd

from recommender import (
    load_videos,
    create_tfidf_model,
    create_similarity_matrix,
    create_user_profile,
    recommend_for_user,
)

# Load videos
videos = load_videos()


# Load user interactions
interactions = pd.read_csv(
    "data/interactions.csv"
)


# Create one shared TF-IDF model
vectorizer, tfidf_matrix = (
    create_tfidf_model(
        videos
    )
)


# Create video-to-video similarity matrix
similarity_matrix = (
    create_similarity_matrix(
        tfidf_matrix
    )
)


print("\nDataset:")
print(
    f"{len(videos)} videos"
)


print("\nUser interactions:")
print(interactions)


# Create user profile
user_profile = create_user_profile(
    videos,
    interactions,
    tfidf_matrix,
)


if user_profile is None:

    print(
        "\nNo watched videos found."
    )

else:

    print(
        "\nUser profile created!"
    )

    print(
        "User profile shape:"
    )

    print(
        user_profile.shape
    )


print(
    "\nTF-IDF matrix shape:"
)

print(
    tfidf_matrix.shape
)


print(
    "\nSimilarity matrix shape:"
)

print(
    similarity_matrix.shape
)

if user_profile is not None:

    recommendations = recommend_for_user(
        videos,
        interactions,
        tfidf_matrix,
        user_profile,
        number_of_recommendations=5,
    )

    print(
        "\nPersonalized recommendations:"
    )

    for _, video in recommendations.iterrows():

        print(
            f"\n- {video['title']}"
        )

        print(
            f"  Channel: "
            f"{video['channel']}"
        )

        print(
            f"  Score: "
            f"{video['score']:.3f}"
        )