from typing import Literal
from enum import StrEnum

from sqlalchemy import Subquery, select, func, and_, case, cast, Integer

from src.common.models.beatmaps import Beatmapset, Beatmap
from src.common.models.collections import Collection, CollectionItem, Pack, PackItem

import src.api.grouping_query.yyy_field_groupings as yyy_field_groupings


GroupingType = Literal[
    'collections',
    'packs',
    'artist',
    'overall_difficulty',
    'ranked_year',
    'ranked_month',
    'bpm',
]

class GroupingTypeEnum(StrEnum):
    COLLECTIONS = 'collections',
    PACKS = 'packs',
    ARTIST = 'artist',
    OVERALL_DIFFICULTY = 'overall_difficulty',
    RANKED_YEAR = 'ranked_year',
    RANKED_MONTH = 'ranked_month',
    BPM = 'bpm',


def get_grouping_sq(grouping_type: GroupingTypeEnum):
    if grouping_type == GroupingTypeEnum.COLLECTIONS:
        grouping_sq = yyy_field_groupings.get_collections_grouping_sq()
    
    elif grouping_type == GroupingTypeEnum.PACKS:
        grouping_sq = yyy_field_groupings.get_packs_grouping_sq()

    elif grouping_type == GroupingTypeEnum.ARTIST:
        grouping_sq = yyy_field_groupings.get_artist_grouping_sq()
    
    elif grouping_type == GroupingTypeEnum.OVERALL_DIFFICULTY:
        grouping_sq = yyy_field_groupings.get_overall_difficulty_grouping_sq()

    elif grouping_type == GroupingTypeEnum.RANKED_YEAR:
        grouping_sq = yyy_field_groupings.get_ranked_year_grouping_sq()
    
    elif grouping_type == GroupingTypeEnum.RANKED_MONTH:
        grouping_sq = yyy_field_groupings.get_ranked_month_grouping_sq()

    elif grouping_type == GroupingTypeEnum.BPM:
        grouping_sq = yyy_field_groupings.get_bpm_grouping_sq()

    return grouping_sq


def get_collections_grouping_sq() -> Subquery:    
    collections_grouping_sq = (
        select(
            CollectionItem.beatmap_db_id.label('beatmap_db_id'),
            Collection.id.label('grouping_id'),
            Collection.name.label('bins'), 
        )
        .select_from(Collection)
        .join(CollectionItem, CollectionItem.collection_id == Collection.id)
    )
    
    return collections_grouping_sq


def get_packs_grouping_sq() -> Subquery:    
    packs_grouping_sq = (
        select(
            PackItem.beatmap_db_id.label('beatmap_db_id'),
            Pack.id.label('grouping_id'),
            Pack.name.label('bins'), 
        )
        .select_from(Pack)
        .join(PackItem, PackItem.pack_id == Pack.id)
    )
    
    return packs_grouping_sq


def get_artist_grouping_sq() -> Subquery:
    bins = func.substr(func.lower(Beatmapset.artist), 1, 1)
    
    inner_sq = (
        select(
            func.row_number().over(order_by=bins).label('id'),
            bins.label('bins'),
        )
        .select_from(Beatmapset)
        .group_by(bins)
        .subquery('inner_sq')
    )
    
    artist_grouping_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            inner_sq.c.bins.label('bins'),
        )
        .select_from(Beatmap)
        .join(Beatmapset, Beatmapset.beatmapset_id == Beatmap.beatmapset_id)
        .join(inner_sq, inner_sq.c.bins == bins)
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
    
    overall_difficulty_grouping_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            inner_sq.c.bins.label('bins'),
        )
        .select_from(Beatmap)
        .join(inner_sq, inner_sq.c.bins == bins)
    )
    
    return overall_difficulty_grouping_sq


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
        (Beatmapset.ranked_year == 2027, 20),
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
        (Beatmapset.ranked_year == 2026, '2027'),
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
    
    ranked_year_grouping_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            inner_sq.c.bins.label('bins'),
        )
        .select_from(Beatmap)
        .join(Beatmapset, Beatmapset.beatmapset_id == Beatmap.beatmapset_id)
        .join(inner_sq, inner_sq.c.bins == bins)
    )

    return ranked_year_grouping_sq


def get_ranked_month_grouping_sq() -> Subquery:
    ids = case(  
        (Beatmapset.ranked_month == 1, 0),
        (Beatmapset.ranked_month == 2, 1),
        (Beatmapset.ranked_month == 3, 2),
        (Beatmapset.ranked_month == 4, 3),
        (Beatmapset.ranked_month == 5, 4),
        (Beatmapset.ranked_month == 6, 5),
        (Beatmapset.ranked_month == 7, 6),
        (Beatmapset.ranked_month == 8, 7),
        (Beatmapset.ranked_month == 9, 8),
        (Beatmapset.ranked_month == 10, 9),
        (Beatmapset.ranked_month == 11, 10),
        (Beatmapset.ranked_month == 12, 11),
    )

    bins = case(  
        (Beatmapset.ranked_month == 1, 'Jan'),
        (Beatmapset.ranked_month == 2, 'Feb'),
        (Beatmapset.ranked_month == 3, 'Mar'),
        (Beatmapset.ranked_month == 4, 'Apr'),
        (Beatmapset.ranked_month == 5, 'May'),
        (Beatmapset.ranked_month == 6, 'Jun'),
        (Beatmapset.ranked_month == 7, 'Jul'),
        (Beatmapset.ranked_month == 8, 'Aug'),
        (Beatmapset.ranked_month == 9, 'Sep'),
        (Beatmapset.ranked_month == 10, 'Oct'),
        (Beatmapset.ranked_month == 11, 'Nov'),
        (Beatmapset.ranked_month == 12, 'Dec'),
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
    
    ranked_month_grouping_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            inner_sq.c.bins.label('bins'),
        )
        .select_from(Beatmap)
        .join(Beatmapset, Beatmapset.beatmapset_id == Beatmap.beatmapset_id)
        .join(inner_sq, inner_sq.c.bins == bins)
    )

    return ranked_month_grouping_sq


def get_bpm_grouping_sq() -> Subquery:
    bins = cast(func.round((Beatmap.bpm - 5) / 10) * 10, Integer)
    
    inner_sq = (
        select(
            func.row_number().over(order_by=bins).label('id'),
            bins.label('bins'),
        )
        .select_from(Beatmap)
        .group_by(bins)
        .subquery('inner_sq')
    )
    
    bpm_grouping_sq = (
        select(
            Beatmap.id.label('beatmap_db_id'),
            inner_sq.c.id.label('grouping_id'),
            inner_sq.c.bins.label('bins'),
        )
        .select_from(Beatmap)
        .join(inner_sq, inner_sq.c.bins == bins)
    )

    return bpm_grouping_sq
