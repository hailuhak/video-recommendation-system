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


def search_videos(query, max_results=50):
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


def collect_videos(queries, videos_per_query=50):

    all_videos = []

    for query in queries:

        print(f"Searching YouTube for: {query}")

        response = search_videos(
            query,
            videos_per_query,
        )

        videos = extract_video_data(response)

        all_videos.extend(videos)

        print(
            f"Collected {len(videos)} videos for '{query}'"
        )

    return all_videos


def remove_duplicates(videos):

    df = pd.DataFrame(videos)

    df = df.drop_duplicates(
        subset="video_id"
    )

    return df


def save_videos(
    videos,
    filename="data/youtube_videos.csv",
):

    videos.to_csv(
        filename,
        index=False,
    )

    print(
        f"\nSaved {len(videos)} unique videos to {filename}"
    )


if __name__ == "__main__":

    queries = [
        "Python tutorial",
        "JavaScript tutorial",
        "React tutorial",
        "Linux tutorial",
        "Cybersecurity tutorial",
        "Docker tutorial",
        "Machine learning tutorial",
        "Web development tutorial",
    ]

    videos = collect_videos(
        queries,
        videos_per_query=50,
    )

    videos = remove_duplicates(videos)

    save_videos(videos)