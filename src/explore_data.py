import pandas as pd


# Load YouTube videos
videos = pd.read_csv("data/youtube_videos.csv")


# Basic information
print("Dataset shape:")
print(videos.shape)

print("\nColumns:")
print(videos.columns.tolist())

print("\nFirst 5 videos:")
print(videos.head())

print("\nMissing values:")
print(videos.isnull().sum())