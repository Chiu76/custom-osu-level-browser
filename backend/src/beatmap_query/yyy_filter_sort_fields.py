from typing import Literal, get_args

from sqlalchemy import Select, Subquery
from sqlalchemy.orm import InstrumentedAttribute

from src.common.models.beatmaps import Beatmap, BeatmapSet
from src.common.models.scores import Score


FILTER_OPS = Literal['!=', '<', '<=', '>', '>=', '=', '~', '&']


FILTER_SORT_FIELDS = Literal[
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

    # score-related
    'grade',
    'accuracy',
    'played_at',

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
    'rank',
    'acc',
]


def get_beatmap_filter_fields() -> dict[str, InstrumentedAttribute]:
    return {
        'beatmap_id': Beatmap.beatmap_id,
        'beatmap_set_id': Beatmap.beatmap_set_id,
        'mode': Beatmap.mode,
        'bpm': Beatmap.bpm,
        'difficulty_name': Beatmap.difficulty_name,
        'ranked_status': Beatmap.ranked_status,
        'num_hitcircles': Beatmap.num_hitcircles,
        'num_sliders': Beatmap.num_sliders,
        'num_spinners': Beatmap.num_spinners,
        'approach_rate': Beatmap.approach_rate,
        'overall_difficulty': Beatmap.overall_difficulty,
        'circle_size': Beatmap.circle_size,
        'hp_drain': Beatmap.hp_drain,
        ## todo: handling of last_played filtering (db stores unix time ish)
        'last_played': Beatmap.last_played,
        ## todo: normalizing drain_time (db stores seconds) vs total_time (db stores miliseconds)
        'drain_time': Beatmap.drain_time,
        'total_time': Beatmap.total_time,
        'local_offset': Beatmap.local_offset,

        # alternatives
        'diff': Beatmap.difficulty_name,
        'status': Beatmap.ranked_status,
        'hitcircles': Beatmap.num_hitcircles,
        'circles': Beatmap.num_hitcircles,
        'sliders': Beatmap.num_sliders,
        'spinners': Beatmap.num_spinners,
        'ar': Beatmap.approach_rate,
        'od': Beatmap.overall_difficulty,
        'cs': Beatmap.circle_size,
        'hp': Beatmap.hp_drain,
        'offset': Beatmap.local_offset,
    }


def get_beatmap_sort_fields(core_sq: Subquery) -> dict[str, InstrumentedAttribute]:
    return {
        'beatmap_id': core_sq.beatmap_id,
        'beatmap_set_id': core_sq.beatmap_set_id,
        'mode': core_sq.mode,
        'bpm': core_sq.bpm,
        'difficulty_name': core_sq.difficulty_name,
        'ranked_status': core_sq.ranked_status,
        'num_hitcircles': core_sq.num_hitcircles,
        'num_sliders': core_sq.num_sliders,
        'num_spinners': core_sq.num_spinners,
        'approach_rate': core_sq.approach_rate,
        'overall_difficulty': core_sq.overall_difficulty,
        'circle_size': core_sq.circle_size,
        'hp_drain': core_sq.hp_drain,
        ## todo: handling of last_played filtering (db stores unix time ish)
        'last_played': core_sq.last_played,
        ## todo: normalizing drain_time (db stores seconds) vs total_time (db stores miliseconds)
        'drain_time': core_sq.drain_time,
        'total_time': core_sq.total_time,
        'local_offset': core_sq.local_offset,

        # alternatives
        'diff': core_sq.difficulty_name,
        'status': core_sq.ranked_status,
        'hitcircles': core_sq.num_hitcircles,
        'circles': core_sq.num_hitcircles,
        'sliders': core_sq.num_sliders,
        'spinners': core_sq.num_spinners,
        'ar': core_sq.approach_rate,
        'od': core_sq.overall_difficulty,
        'cs': core_sq.circle_size,
        'hp': core_sq.hp_drain,
        'offset': core_sq.local_offset,
    }


def get_beatmap_set_filter_fields() -> dict[str, InstrumentedAttribute]:
    return {
        'artist': BeatmapSet.artist,
        'title': BeatmapSet.title,
        'owner': BeatmapSet.owner,
        'song_source': BeatmapSet.song_source,
        'song_tags': BeatmapSet.song_tags,

        # alternatives
        'set_owner': BeatmapSet.owner,
        'set_mapper': BeatmapSet.owner,
        'source': BeatmapSet.song_source,
        'tags': BeatmapSet.song_tags,
    }


def get_beatmap_set_sort_fields(core_sq: Subquery | None = None) -> dict[str, InstrumentedAttribute]:
    return {
        'artist': core_sq.artist,
        'title': core_sq.title,
        'owner': core_sq.owner,
        'song_source': core_sq.song_source,
        'song_tags': core_sq.song_tags,

        # alternatives
        'set_owner': core_sq.owner,
        'set_mapper': core_sq.owner,
        'source': core_sq.song_source,
        'tags': core_sq.song_tags,
    }


def get_score_filter_fields(core_stmt: Select) -> dict[str, InstrumentedAttribute]:
    core_stmt_froms = core_stmt.get_final_froms()[0]
    return {
        'grade': core_stmt_froms.c.corresponding_column(Score.grade),
        'accuracy': core_stmt_froms.c.corresponding_column(Score.accuracy),
        'played_at': core_stmt_froms.c.corresponding_column(Score.played_at),

        # alternatives
        'rank': core_stmt_froms.c.corresponding_column(Score.accuracy),
        'acc': core_stmt_froms.c.corresponding_column(Score.accuracy),
    }

    
def get_score_sort_fields(core_sq: Subquery) -> dict[str, InstrumentedAttribute]:
    return {
        'grade': core_sq.c.grade,
        'accuracy': core_sq.c.accuracy,
        'played_at': core_sq.c.played_at,

        # alternatives
        'rank': core_sq.c.grade,
        'acc': core_sq.c.accuracy,
    }


## todo: separate sort and filter column getter logic to make it clearer and easier to understand
def get_column__filter_field(field: FILTER_SORT_FIELDS, core_stmt: Select | None = None) -> InstrumentedAttribute:
    filter_field_columns = get_beatmap_filter_fields() | get_beatmap_set_filter_fields() | get_score_filter_fields(core_stmt)

    if field not in get_args(FILTER_SORT_FIELDS):
        raise ValueError(f'Received invalid field value, not present in FILTER_SORT_FIELDS mapping: {field}')

    return filter_field_columns[field]


def get_column__sort_field(
    field: FILTER_SORT_FIELDS, 
    core_sq: Subquery, 
) -> InstrumentedAttribute:
    sort_field_columns = get_beatmap_sort_fields(core_sq) | get_beatmap_set_sort_fields(core_sq) | get_score_sort_fields(core_sq)

    if field not in get_args(FILTER_SORT_FIELDS):
        raise ValueError(f'Received invalid field value, not present in FILTER_SORT_FIELDS mapping: {field}')

    return sort_field_columns[field]
