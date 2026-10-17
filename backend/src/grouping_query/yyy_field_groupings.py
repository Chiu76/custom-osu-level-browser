from sqlalchemy import Subquery, select, func, and_, case

from src.common.models.beatmaps import BeatmapSet, Beatmap


def get_artist_grouping_sq() -> Subquery:
    first_char = func.substr(func.lower(BeatmapSet.artist), 1, 1).label('first_char')
    
    inner_sq = (
        select(
            func.row_number().over(order_by=first_char).label('id'),
            first_char,
        )
        .select_from(BeatmapSet)
        .group_by(first_char)
        .subquery('inner_sq')
    )
    
    artist_grouping_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            BeatmapSet.artist, 
        )
        .select_from(Beatmap)
        .join(BeatmapSet, BeatmapSet.beatmap_set_id == Beatmap.beatmap_set_id)
        .join(inner_sq, first_char == inner_sq.c.first_char)
    )
    
    return artist_grouping_sq


def get_overall_difficulty_grouping_sq() -> Subquery:
    bins = case(  
        (Beatmap.overall_difficulty < 1, '0-1'),
        (and_(Beatmap.overall_difficulty >= 1, Beatmap.overall_difficulty < 2), '1-2'),
        (and_(Beatmap.overall_difficulty >= 2, Beatmap.overall_difficulty < 3), '2-3'),
        (and_(Beatmap.overall_difficulty >= 3, Beatmap.overall_difficulty < 4), '3-4'),
        (and_(Beatmap.overall_difficulty >= 4, Beatmap.overall_difficulty < 5), '4-5'),
        (and_(Beatmap.overall_difficulty >= 5, Beatmap.overall_difficulty < 6), '5-6'),
        (and_(Beatmap.overall_difficulty >= 6, Beatmap.overall_difficulty < 7), '6-7'),
        (and_(Beatmap.overall_difficulty >= 7, Beatmap.overall_difficulty < 8), '7-8'),
        (and_(Beatmap.overall_difficulty >= 8, Beatmap.overall_difficulty < 9), '8-9'),
        (and_(Beatmap.overall_difficulty >= 9, Beatmap.overall_difficulty < 10), '9-10'),
        else_='10',
    )
    
    inner_sq = (
        select(
            func.row_number().over(order_by=bins).label('id'),
            bins.label('bins'),
        )
        .select_from(Beatmap)
        .group_by(bins)
        .subquery('inner_sq')
    )
    
    overall_difficulty_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            inner_sq.c.bins,
            Beatmap.overall_difficulty, 
        )
        .select_from(Beatmap)
        .join(inner_sq, inner_sq.c.bins == bins)
    )
    
    return overall_difficulty_sq
