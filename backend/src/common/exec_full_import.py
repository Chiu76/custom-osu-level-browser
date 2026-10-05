import sys

from src.ingestion.jobs.full_import import run_job__full_import

from .db import Model, engine
from .models.beatmaps import BeatmapSet, Beatmap
from .models.state import State

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "recreate_db":
        Model.metadata.drop_all(engine)
        Model.metadata.create_all(engine)

    run_job__full_import()