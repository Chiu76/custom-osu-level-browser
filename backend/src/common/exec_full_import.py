import sys

from src.ingestion.jobs.full_import import full_import

from .db import Model, engine
from .models.state import State
from .models.beatmaps import BeatmapSet, Beatmap
from .models.collections import Collection, CollectionItem


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'update_db':
            Model.metadata.create_all(engine)
        if sys.argv[1] == 'recreate_db':
            Model.metadata.drop_all(engine)
            Model.metadata.create_all(engine)

    full_import()