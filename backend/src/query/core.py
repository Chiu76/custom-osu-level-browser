from sqlalchemy import Select, select, or_, and_
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas.specs import CoreSpecs, StarRatingSpec, AttachedScoreSpec, OnlineDetailsSpec, SourceSpec, Filter, FilterSpec

from .filter_sort_fields import get_column__filter_sort_field

from src.common.models.beatmaps import Beatmap, BeatmapSet



def apply_core_specs(initial_stmt: Select, core_specs: CoreSpecs):
    core_stmt = initial_stmt

    core_stmt = apply_star_rating(core_stmt, core_specs.star_rating_spec)
    core_stmt = apply_attached_score(core_stmt, core_specs.attached_score_spec)
    core_stmt = apply_online_details(core_stmt, core_specs.online_details_spec)
    core_stmt = apply_source(core_stmt, core_specs.source_spec)
    core_stmt = apply_filter(core_stmt, core_specs.filter_spec)

    return core_stmt


def apply_star_rating(stmt: Select, star_rating_spec: StarRatingSpec) -> Select:
    return stmt


def apply_attached_score(stmt: Select, attached_score_spec: AttachedScoreSpec) -> Select:
    return stmt


def apply_online_details(stmt: Select, online_details_spec: OnlineDetailsSpec) -> Select:
    return stmt


def apply_source(stmt: Select, source_spec: SourceSpec) -> Select:
    if source_spec.type == 'local_beatmaps':
        pass
    return stmt


def _get_filter_condition(filter: Filter):
    field_column = get_column__filter_sort_field(filter.field)

    if field_column is None:
        return None

    # case for each possible op
    # since op is already validated by FastAPI, no default case or final return
    match filter.op:
        case '!=':
            return field_column.not_ilike(f'%{filter.value}%')
        case '<':
            return field_column < filter.value
        case '<=':
            return field_column <= filter.value
        case '>':
            return field_column > filter.value
        case '>=':
            return field_column >= filter.value
        case '=':
            return field_column.ilike(f'%{filter.value}%')


def apply_filter(stmt: Select, filter_spec: FilterSpec) -> Select:
    if not filter_spec.filters:
        return stmt

    conditions = [_get_filter_condition(f) for f in filter_spec.filters]
    stmt = stmt.where(and_(*conditions))

    return stmt
