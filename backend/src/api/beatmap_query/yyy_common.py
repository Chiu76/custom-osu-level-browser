from datetime import datetime
import time

from sqlalchemy import Exists, select, exists, and_
from sqlalchemy.orm import InstrumentedAttribute

import src.api.grouping_query.yyy_field_groupings as yyy_field_groupings

from src.common.models.collections import CollectionItem


def exists_in_collections_grouping(beatmap_db_id_col: InstrumentedAttribute, collection_id: int) -> Exists:
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


def exists_in_artist_grouping(beatmap_db_id_col: InstrumentedAttribute, grouping_id: int) -> Exists:
    artist_grouping_sq = yyy_field_groupings.get_artist_grouping_sq()
    return (
        exists(
            select(1)
            .select_from(artist_grouping_sq)
            .where(and_(
                artist_grouping_sq.c.beatmap_db_id == beatmap_db_id_col,
                artist_grouping_sq.c.grouping_id == grouping_id,
            ))
        )
    )


def exists_in_overall_difficulty_grouping(beatmap_db_id_col: InstrumentedAttribute, grouping_id: int) -> Exists:
    overall_difficulty_grouping_sq = yyy_field_groupings.get_overall_difficulty_grouping_sq()
    return (
        exists(
            select(1)
            .select_from(overall_difficulty_grouping_sq)
            .where(and_(
                overall_difficulty_grouping_sq.c.beatmap_db_id == beatmap_db_id_col,
                overall_difficulty_grouping_sq.c.grouping_id == grouping_id,
            ))
        )
    )


def exists_in_ranked_year_grouping(beatmap_db_id_col: InstrumentedAttribute, grouping_id: int) -> Exists:
    ranked_year_grouping_sq = yyy_field_groupings.get_ranked_year_grouping_sq()
    return (
        exists(
            select(1)
            .select_from(ranked_year_grouping_sq)
            .where(and_(
                ranked_year_grouping_sq.c.beatmap_db_id == beatmap_db_id_col,
                ranked_year_grouping_sq.c.grouping_id == grouping_id,
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
