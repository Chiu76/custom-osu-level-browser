from sqlalchemy import Select, Subquery, select, or_, and_, desc
from sqlalchemy.orm import InstrumentedAttribute

from .schemas.specs import PresentationSpecs, GroupingSpec, SearchSpec, Sort, SortSpec, LocalBeatmapsIdentifier

from .yyy_filter_sort_fields import get_column__sort_field

from .yyy_common import exists_in_grouping
import src.api.grouping_query.yyy_field_groupings as yyy_field_groupings

from src.api.grouping_query.enums import GroupingTypeEnum


def apply_presentation_specs(core_stmt: Select, presentation_specs: PresentationSpecs):
    core_sq = core_stmt.subquery('core_sq')

    beatmap_query_stmt = select(core_sq)
    beatmap_query_stmt = apply_search(beatmap_query_stmt, core_sq, presentation_specs.search_spec)
    beatmap_query_stmt = apply_grouping(beatmap_query_stmt, core_sq, presentation_specs.grouping_specs)
    beatmap_query_stmt = apply_sort(beatmap_query_stmt, core_sq, presentation_specs.sort_spec)

    return beatmap_query_stmt


def apply_search(stmt: Select, core_sq: Subquery, search_spec: SearchSpec) -> Select:
    clauses = []
    
    for q in search_spec.queries:
        clauses.append(
            or_(
                ## todo: eventually, have the searchable columns defined somewhere else? and destructure them here only
                core_sq.c.beatmap_id.ilike(f'%{q}%'),
                core_sq.c.beatmapset_id.ilike(f'%{q}%'),
                core_sq.c.difficulty_name.ilike(f'%{q}%'),
                core_sq.c.artist.ilike(f'%{q}%'),
                core_sq.c.title.ilike(f'%{q}%'),
                core_sq.c.owner.ilike(f'%{q}%'),
                core_sq.c.song_source.ilike(f'%{q}%'),
                core_sq.c.song_tags.ilike(f'%{q}%'),
            )
        )

    if clauses:
        stmt = stmt.where(and_(*clauses))
    
    return stmt


def apply_grouping(stmt: Select, core_sq: Subquery, grouping_specs: list[GroupingSpec]) -> Select:
    clauses = []

    for grouping_spec in grouping_specs:
        if grouping_spec.type == GroupingTypeEnum.COLLECTIONS:
            exists_stmt = exists_in_grouping(
                yyy_field_groupings.get_collections_grouping_sq, 
                core_sq.c.beatmap_db_id, 
                grouping_spec.id,
            )
            clauses.append(exists_stmt)

        elif grouping_spec.type == GroupingTypeEnum.PACKS:
            exists_stmt = exists_in_grouping(
                yyy_field_groupings.get_packs_grouping_sq, 
                core_sq.c.beatmap_db_id, 
                grouping_spec.id,
            )
            clauses.append(exists_stmt)

        elif grouping_spec.type == GroupingTypeEnum.ARTIST:
            exists_stmt = exists_in_grouping(
                yyy_field_groupings.get_artist_grouping_sq, 
                core_sq.c.beatmap_db_id, 
                grouping_spec.id,
            )
            clauses.append(exists_stmt)
                    
        elif grouping_spec.type == GroupingTypeEnum.OVERALL_DIFFICULTY:
            exists_stmt = exists_in_grouping(
                yyy_field_groupings.get_overall_difficulty_grouping_sq, 
                core_sq.c.beatmap_db_id, 
                grouping_spec.id,
            )
            clauses.append(exists_stmt)   

        elif grouping_spec.type == GroupingTypeEnum.RANKED_YEAR:
            exists_stmt = exists_in_grouping(
                yyy_field_groupings.get_ranked_year_grouping_sq, 
                core_sq.c.beatmap_db_id, 
                grouping_spec.id,
            )
            clauses.append(exists_stmt)

        elif grouping_spec.type == GroupingTypeEnum.RANKED_MONTH:
            exists_stmt = exists_in_grouping(
                yyy_field_groupings.get_ranked_month_grouping_sq, 
                core_sq.c.beatmap_db_id, 
                grouping_spec.id,
            )
            clauses.append(exists_stmt)

    if clauses:
        stmt = stmt.where(or_(*clauses))
    
    return stmt


def _get_default_sort_columns(core_sq: Subquery) -> list[InstrumentedAttribute]:
    return [
        get_column__sort_field('artist', core_sq),
        get_column__sort_field('title', core_sq),
        get_column__sort_field('beatmapset_id', core_sq),
    ]


def _get_sort_columns(sort: Sort, core_sq: Subquery):
    field_column = get_column__sort_field(sort.field, core_sq)
    if sort.dir == 'desc': field_column = desc(field_column)
    return field_column


def apply_sort(stmt: Select, core_sq: Subquery, sort_spec: SortSpec) -> Select:
    sort_columns = [_get_sort_columns(s, core_sq) for s in sort_spec.sort_columns]
    
    if sort_columns:
        stmt = stmt.order_by(*sort_columns)
    else:
        stmt = stmt.order_by(*_get_default_sort_columns(core_sq))

    return stmt
