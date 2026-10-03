import os

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
results = search_videos("Python tutorial", 5)

videos = extract_video_data(results)

for video in videos:
    print("\nVideo:")
    print("ID:", video["video_id"])
    print("Title:", video["title"])
    print("Channel:", video["channel"])
    print("Published:", video["published_at"])
    print("Thumbnail:", video["thumbnail"])