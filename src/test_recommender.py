from recommender import (
    load_videos,
    create_similarity_matrix,
    recommend_videos,
)


videos = load_videos()

similarity_matrix = (
    create_similarity_matrix(
        videos
    )
)


first_video = videos.iloc[0]

print(
    "\nWatching:"
)

print(
    first_video["title"]
)


recommendations = recommend_videos(
    videos,
    similarity_matrix,
    first_video["video_id"],
    number_of_recommendations=5,
)


print(
    "\nRecommendations:"
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
        f"  Similarity: "
        f"{video['similarity']:.3f}"
    )