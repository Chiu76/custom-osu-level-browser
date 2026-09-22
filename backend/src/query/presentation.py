import json

from sqlalchemy import Select, Subquery, select, or_, and_, desc
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas.specs import PresentationSpecs, GroupingSpec, SearchSpec, Sorting, SortingSpec, LocalBeatmapsIdentifier

from .filter_sort_fields import get_column__filter_sort_field

from src.common.models.beatmaps import Beatmap, BeatmapSet


def apply_presentation_specs(core_stmt: Select, presentation_specs: PresentationSpecs):
    core_stmt_sq = core_stmt.subquery('core_stmt_sq')

    beatmap_query_stmt = select(core_stmt_sq)
    beatmap_query_stmt = apply_search(beatmap_query_stmt, presentation_specs.search_spec)
    beatmap_query_stmt = apply_grouping(beatmap_query_stmt, presentation_specs.grouping_spec)
    beatmap_query_stmt = apply_sorting(beatmap_query_stmt, core_stmt_sq, presentation_specs.sorting_spec)

    return beatmap_query_stmt


def apply_search(stmt: Select, search_spec: SearchSpec) -> Select:
    if not search_spec.q:
        return stmt

    q = search_spec.q
    stmt = stmt.where(
        or_(
            ## todo: eventually, have the searchable columns defined somewhere else? and destructure them here only
            Beatmap.beatmap_id.ilike(f'%{q}%'),
            Beatmap.beatmap_set_id.ilike(f'%{q}%'),
            Beatmap.difficulty_name.ilike(f'%{q}%'),
            BeatmapSet.artist.ilike(f'%{q}%'),
            BeatmapSet.title.ilike(f'%{q}%'),
            BeatmapSet.owner.ilike(f'%{q}%'),
            BeatmapSet.song_source.ilike(f'%{q}%'),
            BeatmapSet.song_tags.ilike(f'%{q}%'),
        )
    )
    
    return stmt


def apply_grouping(stmt: Select, grouping_spec: GroupingSpec) -> Select:
    if grouping_spec.type == 'local_beatmaps':
        pass
    return stmt


def _get_default_sorting_columns(core_stmt_sq) -> list[InstrumentedAttribute]:
    return [
        get_column__filter_sort_field('artist', core_stmt_sq),
        get_column__filter_sort_field('title', core_stmt_sq),
        get_column__filter_sort_field('beatmap_set_id', core_stmt_sq),
    ]


def _get_sorting_columns(sorting: Sorting, core_stmt_sq):
    field_column = get_column__filter_sort_field(sorting.field, core_stmt_sq)
    if sorting.dir == 'desc':
        field_column = desc(field_column)
    return field_column


def apply_sorting(stmt: Select, core_stmt_sq, sorting_spec: SortingSpec) -> Select:
    sorting_columns = [_get_sorting_columns(s, core_stmt_sq) for s in sorting_spec.sortings]
    
    if sorting_columns:
        stmt = stmt.order_by(*sorting_columns)
    else:
        stmt = stmt.order_by(*_get_default_sorting_columns(core_stmt_sq))

    return stmt
