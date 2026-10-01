from typing import Literal, get_args

from sqlalchemy import Select, Subquery
from sqlalchemy.orm import InstrumentedAttribute

from src.common.models.beatmaps import Beatmap, BeatmapSet


FILTER_SORT_FIELD = Literal[
    'beatmap_id',
    'beatmap_set_id',
    'mode',
    'bpm',
    'difficulty_name',
    'ranked_status',
    'num_hitcircles',
    'num_sliders',
    'num_spinners',
    'approach_rate',
    'overall_difficulty',
    'circle_size',
    'hp_drain',
    'last_played',
    'drain_time',
    'total_time',
    'local_offset',
    'artist',
    'title',
    'owner',
    'song_source',
    'song_tags',

    # alternatives
    'diff',
    'status',
    'hitcircles',
    'circles',
    'sliders',
    'spinners',
    'ar',
    'od',
    'cs',
    'hp',
    'offset',
    'set_owner',
    'set_mapper',
    'source',
    'tags',
]


def get_beatmap_fields(sq: Subquery = None) -> dict[str, InstrumentedAttribute]:
    table_or_query = Beatmap if sq is None else sq.c
    return {
        'beatmap_id': table_or_query.beatmap_id,
        'beatmap_set_id': table_or_query.beatmap_set_id,
        'mode': table_or_query.mode,
        'bpm': table_or_query.bpm,
        'difficulty_name': table_or_query.difficulty_name,
        'ranked_status': table_or_query.ranked_status,
        'num_hitcircles': table_or_query.num_hitcircles,
        'num_sliders': table_or_query.num_sliders,
        'num_spinners': table_or_query.num_spinners,
        'approach_rate': table_or_query.approach_rate,
        'overall_difficulty': table_or_query.overall_difficulty,
        'circle_size': table_or_query.circle_size,
        'hp_drain': table_or_query.hp_drain,
        ## todo: handling of last_played filtering (db stores unix time ish)
        'last_played': table_or_query.last_played,
        ## todo: normalizing drain_time (db stores seconds) vs total_time (db stores miliseconds)
        'drain_time': table_or_query.drain_time,
        'total_time': table_or_query.total_time,
        'local_offset': table_or_query.local_offset,

        # alternatives
        'diff': table_or_query.difficulty_name,
        'status': table_or_query.ranked_status,
        'hitcircles': table_or_query.num_hitcircles,
        'circles': table_or_query.num_hitcircles,
        'sliders': table_or_query.num_sliders,
        'spinners': table_or_query.num_spinners,
        'ar': table_or_query.approach_rate,
        'od': table_or_query.overall_difficulty,
        'cs': table_or_query.circle_size,
        'hp': table_or_query.hp_drain,
        'offset': table_or_query.local_offset,
    }


def get_beatmap_set_fields(sq: Subquery = None) -> dict[str, InstrumentedAttribute]:
    table_or_query = BeatmapSet if sq is None else sq.c
    return {
        'artist': table_or_query.artist,
        'title': table_or_query.title,
        'owner': table_or_query.owner,
        'song_source': table_or_query.song_source,
        'song_tags': table_or_query.song_tags,

        # alternatives
        'set_owner': table_or_query.owner,
        'set_mapper': table_or_query.owner,
        'source': table_or_query.song_source,
        'tags': table_or_query.song_tags,
    }


def get_column__filter_sort_field(field: FILTER_SORT_FIELD, sq: Subquery = None) -> InstrumentedAttribute:
    filter_sort_field_columns = get_beatmap_fields(sq) | get_beatmap_set_fields(sq)

    if field not in get_args(FILTER_SORT_FIELD):
        raise(ValueError(f'Received invalid field value, not present in FILTER_FIELD mapping: {field}'))

    return filter_sort_field_columns[field]
