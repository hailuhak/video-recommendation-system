import os
from datetime import datetime, timezone

import pandas as pd


project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


INTERACTIONS_FILE = os.path.join(
    project_root,
    "data",
    "interactions.csv",
)


def record_interaction(
    user_id,
    video_id,
    event_type,
):

    interaction = pd.DataFrame(
        [
            {
                "user_id": user_id,
                "video_id": video_id,
                "event_type": event_type,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
            }
        ]
    )

    interaction.to_csv(
        INTERACTIONS_FILE,
        mode="a",
        header=False,
        index=False,
    )
    