
import os

import pandas as pd
from flask import Flask, render_template


# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(project_root, "templates"),
)


@app.route("/")
def home():
    videos = pd.read_csv(
        os.path.join(project_root, "data", "youtube_videos.csv")
    )

    print(f"Loaded {len(videos)} videos")

    return render_template(
        "index.html",
        videos=videos.to_dict(orient="records"),
    )


if __name__ == "__main__":
 app.run(port=5001, debug=True)
