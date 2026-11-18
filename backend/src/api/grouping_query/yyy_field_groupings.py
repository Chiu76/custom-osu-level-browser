from sqlalchemy import Subquery, select, func, and_, case

from src.common.models.beatmaps import Beatmapset, Beatmap


def get_artist_grouping_sq() -> Subquery:
    first_char = func.substr(func.lower(Beatmapset.artist), 1, 1).label('first_char')
    
    inner_sq = (
        select(
            func.row_number().over(order_by=first_char).label('id'),
            first_char,
        )
        .select_from(Beatmapset)
        .group_by(first_char)
        .subquery('inner_sq')
    )
    
    artist_grouping_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            Beatmapset.artist, 
        )
        .select_from(Beatmap)
        .join(Beatmapset, Beatmapset.beatmapset_id == Beatmap.beatmapset_id)
        .join(inner_sq, first_char == inner_sq.c.first_char)
    )
    
    return artist_grouping_sq


def get_overall_difficulty_grouping_sq() -> Subquery:
    ids = case(  
        (Beatmap.overall_difficulty < 1, 0),
        (and_(Beatmap.overall_difficulty >= 1, Beatmap.overall_difficulty < 2), 1),
        (and_(Beatmap.overall_difficulty >= 2, Beatmap.overall_difficulty < 3), 2),
        (and_(Beatmap.overall_difficulty >= 3, Beatmap.overall_difficulty < 4), 3),
        (and_(Beatmap.overall_difficulty >= 4, Beatmap.overall_difficulty < 5), 4),
        (and_(Beatmap.overall_difficulty >= 5, Beatmap.overall_difficulty < 6), 5),
        (and_(Beatmap.overall_difficulty >= 6, Beatmap.overall_difficulty < 7), 6),
        (and_(Beatmap.overall_difficulty >= 7, Beatmap.overall_difficulty < 8), 7),
        (and_(Beatmap.overall_difficulty >= 8, Beatmap.overall_difficulty < 9), 8),
        (and_(Beatmap.overall_difficulty >= 9, Beatmap.overall_difficulty < 10), 9),
        else_=10,
    )

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
        else_='10+',
    )
    
    inner_sq = (
        select(
            ids.label('id'),
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


def get_ranked_year_grouping_sq() -> Subquery:
    ids = case(  
        (Beatmapset.ranked_year == 2007, 0),
        (Beatmapset.ranked_year == 2008, 1),
        (Beatmapset.ranked_year == 2009, 2),
        (Beatmapset.ranked_year == 2010, 3),
        (Beatmapset.ranked_year == 2011, 4),
        (Beatmapset.ranked_year == 2012, 5),
        (Beatmapset.ranked_year == 2013, 6),
        (Beatmapset.ranked_year == 2014, 7),
        (Beatmapset.ranked_year == 2015, 8),
        (Beatmapset.ranked_year == 2016, 9),
        (Beatmapset.ranked_year == 2017, 10),
        (Beatmapset.ranked_year == 2018, 11),
        (Beatmapset.ranked_year == 2019, 12),
        (Beatmapset.ranked_year == 2020, 13),
        (Beatmapset.ranked_year == 2021, 14),
        (Beatmapset.ranked_year == 2022, 15),
        (Beatmapset.ranked_year == 2023, 16),
        (Beatmapset.ranked_year == 2024, 17),
        (Beatmapset.ranked_year == 2025, 18),
        (Beatmapset.ranked_year == 2026, 19),
    )

    bins = case(  
        (Beatmapset.ranked_year == 2007, '2007'),
        (Beatmapset.ranked_year == 2008, '2008'),
        (Beatmapset.ranked_year == 2009, '2009'),
        (Beatmapset.ranked_year == 2010, '2010'),
        (Beatmapset.ranked_year == 2011, '2011'),
        (Beatmapset.ranked_year == 2012, '2012'),
        (Beatmapset.ranked_year == 2013, '2013'),
        (Beatmapset.ranked_year == 2014, '2014'),
        (Beatmapset.ranked_year == 2015, '2015'),
        (Beatmapset.ranked_year == 2016, '2016'),
        (Beatmapset.ranked_year == 2017, '2017'),
        (Beatmapset.ranked_year == 2018, '2018'),
        (Beatmapset.ranked_year == 2019, '2019'),
        (Beatmapset.ranked_year == 2020, '2020'),
        (Beatmapset.ranked_year == 2021, '2021'),
        (Beatmapset.ranked_year == 2022, '2022'),
        (Beatmapset.ranked_year == 2023, '2023'),
        (Beatmapset.ranked_year == 2024, '2024'),
        (Beatmapset.ranked_year == 2025, '2025'),
        (Beatmapset.ranked_year == 2026, '2026'),
    )
    
    inner_sq = (
        select(
            ids.label('id'),
            bins.label('bins'),
        )
        .select_from(Beatmapset)
        .group_by(bins)
        .subquery('inner_sq')
    )
    
    ranked_year_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            inner_sq.c.bins,
            Beatmap.overall_difficulty, 
        )
        .select_from(Beatmap)
        .join(Beatmapset, Beatmapset.beatmapset_id == Beatmap.beatmapset_id)
        .join(inner_sq, inner_sq.c.bins == bins)
    )

    return ranked_year_sq
