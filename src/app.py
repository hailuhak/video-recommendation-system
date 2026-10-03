
import os

import pandas as pd
from flask import Flask, render_template

from recommender import (
    load_videos,
    create_similarity_matrix,
    recommend_videos,
)

# Get the project root directory
project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


app = Flask(
    __name__,
    template_folder=os.path.join(
        project_root,
        "templates",
    ),
)


@app.route("/")
def home():

    videos = pd.read_csv(
        os.path.join(
            project_root,
            "data",
            "youtube_videos.csv",
        )
    )

    print(f"Loaded {len(videos)} videos")

    return render_template(
        "index.html",
        videos=videos.to_dict(orient="records"),
    )

id="gr3v8a"
@app.route("/video/<video_id>")
def video(video_id):

    videos = load_videos(
        os.path.join(
            project_root,
            "data",
            "youtube_videos.csv",
        )
    )

    similarity_matrix = create_similarity_matrix(
        videos
    )

    selected_video = videos[
        videos["video_id"] == video_id
    ]

    if selected_video.empty:
        return "Video not found", 404

    selected_video = selected_video.iloc[0].to_dict()

    recommendations = recommend_videos(
        videos,
        similarity_matrix,
        video_id,
        number_of_recommendations=3,
    )

    recommendations = recommendations.to_dict(
        orient="records"
    )

    return render_template(
        "video.html",
        video=selected_video,
        recommendations=recommendations,
    )



    videos = pd.read_csv(
        os.path.join(
            project_root,
            "data",
            "youtube_videos.csv",
        )
    )

    selected_video = videos[
        videos["video_id"] == video_id
    ]

    if selected_video.empty:
        return "Video not found", 404

    selected_video = selected_video.iloc[0].to_dict()

    return render_template(
        "video.html",
        video=selected_video,
    )


if __name__ == "__main__":
    app.run(
        port=5001,
        debug=True,
    )

