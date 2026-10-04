import pandas as pd


videos = pd.read_csv(
    "data/youtube_videos.csv"
)


print("Dataset shape:")
print(videos.shape)


print("\nColumns:")
print(videos.columns.tolist())


print("\nFirst 5 videos:")
print(
    videos[
        [
            "video_id",
            "title",
            "channel",
            "published_at",
        ]
    ].head()
)


print("\nMissing values:")
print(
    videos.isnull().sum()
)


print("\nVideos per channel:")
print(
    videos["channel"]
    .value_counts()
    .head(10)
)


print("\nDataset information:")
print(
    videos.info()
)