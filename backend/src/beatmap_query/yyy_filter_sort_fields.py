from typing import Literal

from sqlalchemy import Select, Subquery
from sqlalchemy.orm import InstrumentedAttribute

from src.common.models.beatmaps import Beatmap, BeatmapSet, BeatmapStarRating
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

    'star_rating',

    'num_300s',
    'num_100s',
    'num_50s',
    'num_gekis',
    'num_katus',
    'num_misses',
    'grade',
    'accuracy',
    'replay_score',
    'max_combo',
    'perfect_combo',
    'mods',
    'played_at',
]


FILTER_SORT_FIELDS_ALTERNATIVES = Literal[
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

    
    'sr',
    'stars',

    '300s',
    '100s',
    '50s',
    'gekis',
    'katus',
    'misses',
    'rank',
    'acc',
    'score',
    'combo',
    'is_fc',
    'pfc',
]


def get_beatmap_filter_columns() -> dict[str, InstrumentedAttribute]:
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
        'last_played': Beatmap.last_played,
        ## todo: normalizing drain_time (db stores seconds) vs total_time (db stores miliseconds)
        'drain_time': Beatmap.drain_time,
        'total_time': Beatmap.total_time,
        'local_offset': Beatmap.local_offset,

        'star_rating': BeatmapStarRating.star_rating,

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

        'sr': BeatmapStarRating.star_rating,
        'stars': BeatmapStarRating.star_rating,
    }


def get_beatmap_sort_columns(core_sq: Subquery) -> dict[str, InstrumentedAttribute]:
    return {
        'beatmap_id': core_sq.c.beatmap_id,
        'beatmap_set_id': core_sq.c.beatmap_set_id,
        'mode': core_sq.c.mode,
        'bpm': core_sq.c.bpm,
        'difficulty_name': core_sq.c.difficulty_name,
        'ranked_status': core_sq.c.ranked_status,
        'num_hitcircles': core_sq.c.num_hitcircles,
        'num_sliders': core_sq.c.num_sliders,
        'num_spinners': core_sq.c.num_spinners,
        'approach_rate': core_sq.c.approach_rate,
        'overall_difficulty': core_sq.c.overall_difficulty,
        'circle_size': core_sq.c.circle_size,
        'hp_drain': core_sq.c.hp_drain,
        'last_played': core_sq.c.last_played,
        ## todo: normalizing drain_time (db stores seconds) vs total_time (db stores miliseconds)
        'drain_time': core_sq.c.drain_time,
        'total_time': core_sq.c.total_time,
        'local_offset': core_sq.c.local_offset,

        'star_rating': core_sq.c.star_rating,

        # alternatives
        'diff': core_sq.c.difficulty_name,
        'status': core_sq.c.ranked_status,
        'hitcircles': core_sq.c.num_hitcircles,
        'circles': core_sq.c.num_hitcircles,
        'sliders': core_sq.c.num_sliders,
        'spinners': core_sq.c.num_spinners,
        'ar': core_sq.c.approach_rate,
        'od': core_sq.c.overall_difficulty,
        'cs': core_sq.c.circle_size,
        'hp': core_sq.c.hp_drain,
        'offset': core_sq.c.local_offset,

        'sr': core_sq.c.star_rating,
        'stars': core_sq.c.star_rating,
    }


def get_beatmap_set_filter_columns() -> dict[str, InstrumentedAttribute]:
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


def get_beatmap_set_sort_columns(core_sq: Subquery | None = None) -> dict[str, InstrumentedAttribute]:
    return {
        'artist': core_sq.c.artist,
        'title': core_sq.c.title,
        'owner': core_sq.c.owner,
        'song_source': core_sq.c.song_source,
        'song_tags': core_sq.c.song_tags,

        # alternatives
        'set_owner': core_sq.c.owner,
        'set_mapper': core_sq.c.owner,
        'source': core_sq.c.song_source,
        'tags': core_sq.c.song_tags,
    }


def get_score_filter_columns(core_stmt: Select) -> dict[str, InstrumentedAttribute]:
    core_stmt_froms = core_stmt.get_final_froms()[0]
    return {
        'num_300s': core_stmt_froms.c.corresponding_column(Score.num_300s),
        'num_100s': core_stmt_froms.c.corresponding_column(Score.num_100s),
        'num_50s': core_stmt_froms.c.corresponding_column(Score.num_50s),
        'num_gekis': core_stmt_froms.c.corresponding_column(Score.num_gekis),
        'num_katus': core_stmt_froms.c.corresponding_column(Score.num_katus),
        'num_missess': core_stmt_froms.c.corresponding_column(Score.num_misses),
        'grade': core_stmt_froms.c.corresponding_column(Score.grade),
        'accuracy': core_stmt_froms.c.corresponding_column(Score.accuracy),
        'replay_score': core_stmt_froms.c.corresponding_column(Score.replay_score),
        'max_combo': core_stmt_froms.c.corresponding_column(Score.max_combo),
        'perfect_combo': core_stmt_froms.c.corresponding_column(Score.perfect_combo),
        'mods': core_stmt_froms.c.corresponding_column(Score.mods),
        'played_at': core_stmt_froms.c.corresponding_column(Score.played_at),

        # alternatives
        '300s': core_stmt_froms.c.corresponding_column(Score.num_300s),
        '100s': core_stmt_froms.c.corresponding_column(Score.num_100s),
        '50s': core_stmt_froms.c.corresponding_column(Score.num_50s),
        'gekis': core_stmt_froms.c.corresponding_column(Score.num_gekis),
        'katus': core_stmt_froms.c.corresponding_column(Score.num_katus),
        'misses': core_stmt_froms.c.corresponding_column(Score.num_misses),
        'rank': core_stmt_froms.c.corresponding_column(Score.grade),
        'acc': core_stmt_froms.c.corresponding_column(Score.accuracy),
        'score': core_stmt_froms.c.corresponding_column(Score.replay_score),
        'combo': core_stmt_froms.c.corresponding_column(Score.max_combo),
        'is_fc': core_stmt_froms.c.corresponding_column(Score.perfect_combo),
        'pfc': core_stmt_froms.c.corresponding_column(Score.perfect_combo),
    }

    
def get_score_sort_columns(core_sq: Subquery) -> dict[str, InstrumentedAttribute]:
    return {
        'num_300s': core_sq.c.num_300s,
        'num_100s': core_sq.c.num_100s,
        'num_50s': core_sq.c.num_50s,
        'num_gekis': core_sq.c.num_gekis,
        'num_katus': core_sq.c.num_katus,
        'num_misses': core_sq.c.num_misses,
        'grade': core_sq.c.grade,
        'accuracy': core_sq.c.accuracy,
        'replay_score': core_sq.c.replay_score,
        'max_combo': core_sq.c.max_combo,
        'perfect_combo': core_sq.c.perfect_combo,
        'mods': core_sq.c.mods,
        'played_at': core_sq.c.played_at,

        # alternatives
        'rank': core_sq.c.grade,
        'acc': core_sq.c.accuracy,
        '300s': core_sq.c.num_300s,
        '100s': core_sq.c.num_100s,
        '50s': core_sq.c.num_50s,
        'gekis': core_sq.c.num_gekis,
        'katus': core_sq.c.num_katus,
        'misses': core_sq.c.num_misses,
        'rank': core_sq.c.grade,
        'acc': core_sq.c.accuracy,
        'score': core_sq.c.replay_score,
        'combo': core_sq.c.max_combo,
        'is_fc': core_sq.c.perfect_combo,
        'pfc': core_sq.c.perfect_combo,
    }


def get_column__filter_field(
    field: FILTER_SORT_FIELDS | FILTER_SORT_FIELDS_ALTERNATIVES, 
    core_stmt: Select
) -> InstrumentedAttribute:
    filter_field_columns = get_beatmap_filter_columns() | get_beatmap_set_filter_columns() | get_score_filter_columns(core_stmt)

    if field not in filter_field_columns.keys():
        raise ValueError(f'Received invalid field value, not present in `filter_field_columns` mapping: {field}')

    return filter_field_columns[field]


def get_column__sort_field(
    field: FILTER_SORT_FIELDS | FILTER_SORT_FIELDS_ALTERNATIVES, 
    core_sq: Subquery, 
) -> InstrumentedAttribute:
    sort_field_columns = get_beatmap_sort_columns(core_sq) | get_beatmap_set_sort_columns(core_sq) | get_score_sort_columns(core_sq)

    if field not in sort_field_columns.keys():
        raise ValueError(f'Received invalid field value, not present in `sort_field_columns` mapping: {field}')

    return sort_field_columns[field]
