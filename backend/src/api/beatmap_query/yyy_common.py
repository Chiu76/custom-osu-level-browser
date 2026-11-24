from typing import Callable
from datetime import datetime
import time

from sqlalchemy import Exists, select, exists, and_
from sqlalchemy.orm import InstrumentedAttribute

from src.api.grouping_query.yyy_field_groupings import GroupingTypeEnum, get_grouping_sq


def exists_in_grouping(grouping_type: GroupingTypeEnum, beatmap_db_id_col: InstrumentedAttribute, grouping_id: int) -> Exists:
    grouping_sq = get_grouping_sq(grouping_type)
    return (
        exists(
            select(1)
            .select_from(grouping_sq)
            .where(and_(
                grouping_sq.c.beatmap_db_id == beatmap_db_id_col,
                grouping_sq.c.grouping_id == grouping_id,
            ))
        )
    )


def date_input_to_posix(value):
    dt = None
    for format in ['%Y.%m.%d', '%Y.%m', '%Y']:
        try:
            dt = datetime.strptime(value, format)
        except ValueError:
            pass
    if dt is None:
        raise ValueError('Invalid date string input')
    return time.mktime(dt.timetuple())
