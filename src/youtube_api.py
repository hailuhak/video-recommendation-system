import os

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=youtube_api_key,
)


def search_videos(query, max_results=10):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results,
    )

    response = request.execute()

    return response


def extract_video_data(response):
    videos = []

    for item in response["items"]:
        video = {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
        }

        videos.append(video)

    return videos


def save_videos(videos, filename="data/youtube_videos.csv"):
    df = pd.DataFrame(videos)

    df.to_csv(filename, index=False)

    print(f"Saved {len(df)} videos to {filename}")


# Search YouTube
results = search_videos("Python tutorial", 5)

# Extract useful information
videos = extract_video_data(results)

# Save the data
save_videos(videos)


# Display the collected videos
for video in videos:
    print("\nVideo:")
    print("ID:", video["video_id"])
    print("Title:", video["title"])
    print("Channel:", video["channel"])
    print("Published:", video["published_at"])
    print("Thumbnail:", video["thumbnail"])

