from sqlalchemy import Select, Subquery, select, or_, and_
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas.specs import CoreSpecs, StarRatingSpec, AttachedScoreSpec, OnlineDetailsSpec, SourceSpec, Filter, FilterSpec

import src.beatmap_query.yyy_filter_sort_fields as filter_sort_fields

from src.common.models.beatmaps import Beatmap

import src.score_query.zzz_score_sq as zzz_score_sq

from .yyy_common import exists_in_collection, date_input_to_posix


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
    score_sq = zzz_score_sq.get_score_sq(attached_score_spec.score_sq_spec)
    
    stmt = stmt.add_columns(*score_sq.c)
    
    if attached_score_spec.score_required:
        stmt_join_or_outerjoin = stmt.join  
    else:
        stmt_join_or_outerjoin = stmt.outerjoin
    
    return stmt_join_or_outerjoin(score_sq, score_sq.c.beatmap_db_id == Beatmap.id)


def apply_online_details(stmt: Select, online_details_spec: OnlineDetailsSpec) -> Select:
    return stmt


def apply_source(stmt: Select, source_spec: SourceSpec) -> Select:
    if source_spec.type == 'local_beatmaps':
        pass
    elif source_spec.type == 'collections':
        collection_id = source_spec.id
        stmt = stmt.where(exists_in_collection(Beatmap.id, collection_id))
    return stmt


def _get_filter_condition(stmt: Select, filter: Filter):
    field_column = filter_sort_fields.get_column__filter_field(field=filter.field, core_stmt=stmt)
    print("coloi: ", field_column)

    if field_column is None:
        return None

    match filter.field:
        case 'played_at':
            try:
                value = date_input_to_posix(filter.value)
            except ValueError as e:
                return None
        case _:
            value = filter.value

    # case for each possible op
    # already validated by FastAPI, so no default case or final return
    match filter.op:
        case '!=':
            return field_column.not_ilike(f'%{value}%')
        case '<':
            return field_column < value
        case '<=':
            return field_column <= value
        case '>':
            return field_column > value
        case '>=':
            return field_column >= value
        case '=':
            return field_column.ilike(f'%{value}%')
        case '~':
            try:
                value = int(value)
                return and_(field_column >= value - 5, field_column <= value + 5)
            except ValueError:
                return None
        case '&':
            try:
                value = int(value)
                return and_(field_column >= value - 1, field_column <= value + 1)
            except ValueError:
                return None


def apply_filter(stmt: Select, filter_spec: FilterSpec) -> Select:
    if not filter_spec.filters:
        return stmt

    conditions = []
    for f in filter_spec.filters:
        condition = _get_filter_condition(stmt, f)
        if condition is not None: 
            conditions.append(condition)

    ## todo: eventually allow either AND, OR, maybe parentheses within filter contents
    stmt = stmt.where(and_(*conditions))

    return stmt
