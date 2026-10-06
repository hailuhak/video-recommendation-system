import os

from flask import (
    Flask,
    render_template,
    jsonify,
)

from interactions import record_interaction

from recommender import (
    load_videos,
    create_tfidf_model,
    create_similarity_matrix,
    recommend_videos,
)


project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


app = Flask(
    __name__,
    template_folder=os.path.join(
        project_root,
        "templates",
    ),
)


VIDEOS_FILE = os.path.join(
    project_root,
    "data",
    "youtube_videos.csv",
)


@app.route("/")
def home():

    videos = load_videos(
        VIDEOS_FILE
    )

    return render_template(
        "index.html",
        videos=videos.to_dict(
            orient="records"
        ),
    )


@app.route("/video/<video_id>")
def video(video_id):

    videos = load_videos(
        VIDEOS_FILE
    )

    # Create the shared TF-IDF model
    vectorizer, tfidf_matrix = (
        create_tfidf_model(
            videos
        )
    )

    # Create video similarity matrix
    similarity_matrix = (
        create_similarity_matrix(
            tfidf_matrix
        )
    )

    selected_video = videos[
        videos["video_id"] == video_id
    ]

    if selected_video.empty:
        return "Video not found", 404

    # Record the user's view
    record_interaction(
        user_id="user_1",
        video_id=video_id,
        event_type="view",
    )

    selected_video = (
        selected_video
        .iloc[0]
        .to_dict()
    )

    recommendations = recommend_videos(
        videos,
        similarity_matrix,
        video_id,
        number_of_recommendations=3,
    )

    recommendations = (
        recommendations
        .to_dict(
            orient="records"
        )
    )

    return render_template(
        "video.html",
        video=selected_video,
        recommendations=recommendations,
    )


@app.route(
    "/video/<video_id>/like",
    methods=["POST"],
)
def like_video(video_id):

    videos = load_videos(
        VIDEOS_FILE
    )

    selected_video = videos[
        videos["video_id"] == video_id
    ]

    if selected_video.empty:
        return jsonify(
            {
                "error": "Video not found"
            }
        ), 404

    record_interaction(
        user_id="user_1",
        video_id=video_id,
        event_type="like",
    )

    return jsonify(
        {
            "message": "Video liked"
        }
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001,
    )