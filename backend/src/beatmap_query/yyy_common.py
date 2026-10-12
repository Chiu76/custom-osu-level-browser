from datetime import datetime
import time

from sqlalchemy import Exists, select, exists, and_
from sqlalchemy.orm import InstrumentedAttribute

from src.common.models.collections import CollectionItem


def exists_in_collection(beatmap_db_id_col: InstrumentedAttribute, collection_id: int) -> Exists:
    return (
        exists(
            select(1)
            .select_from(CollectionItem)
            .where(and_(
                CollectionItem.beatmap_db_id == beatmap_db_id_col,
                CollectionItem.collection_id == collection_id,
            ))
        )
    )


def date_input_to_posix(value):
    dt = None
    for format in ['%Y-%m-%d', '%Y-%m', '%Y']:
        try:
            dt = datetime.strptime(value, format)
        except ValueError:
            pass
    if dt is None:
        raise ValueError('Invalid date string input')
    return time.mktime(dt.timetuple())