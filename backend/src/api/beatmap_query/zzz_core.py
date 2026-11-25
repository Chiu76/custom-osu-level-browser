from sqlalchemy import Select, and_, or_

from .schemas.specs import CoreSpecs, StarRatingSpec, AttachedScoreSpec, SourceSpec, Filter, FilterSpec

from src.common.models.beatmaps import Beatmap, BeatmapStarRating

import src.api.beatmap_query.yyy_filter_sort_fields as filter_sort_fields
import src.api.score_query.zzz_score_sq as zzz_score_sq
from src.api.score_query.yyy_mods import get_mods_value

from .yyy_common import exists_in_grouping, date_input_to_posix


def apply_core_specs(initial_stmt: Select, core_specs: CoreSpecs):
    core_stmt = initial_stmt

    core_stmt = apply_star_rating(core_stmt, core_specs.star_rating_spec)
    core_stmt = apply_attached_score(core_stmt, core_specs.attached_score_spec)
    core_stmt = apply_source(core_stmt, core_specs.source_specs)
    core_stmt = apply_filter(core_stmt, core_specs.filter_spec)

    return core_stmt


def apply_star_rating(stmt: Select, star_rating_spec: StarRatingSpec) -> Select:
    stmt = stmt.add_columns(
        BeatmapStarRating.star_rating,
        BeatmapStarRating.star_rating_aim,
        BeatmapStarRating.star_rating_speed,
        BeatmapStarRating.star_rating_reading,
    )
    
    return stmt.outerjoin(BeatmapStarRating, and_(
        BeatmapStarRating.beatmap_db_id == Beatmap.id,
        BeatmapStarRating.mode == 0,
        BeatmapStarRating.mods == get_mods_value(star_rating_spec.mods),
    ))


def apply_attached_score(stmt: Select, attached_score_spec: AttachedScoreSpec) -> Select:
    score_sq = zzz_score_sq.get_score_sq(attached_score_spec.score_sq_spec)
    
    stmt = stmt.add_columns(*score_sq.c)
    
    if attached_score_spec.show_beatmaps == 'all':
        stmt = stmt.outerjoin(score_sq, score_sq.c.beatmap_db_id == Beatmap.id)

    elif attached_score_spec.show_beatmaps == 'with-score':
        stmt = stmt.join(score_sq, score_sq.c.beatmap_db_id == Beatmap.id)
        
    elif attached_score_spec.show_beatmaps == 'without-score':
        stmt = (
            stmt
                .outerjoin(score_sq, score_sq.c.beatmap_db_id == Beatmap.id)
                .where(score_sq.c.beatmap_db_id == None)
        )

    return stmt


def apply_source(stmt: Select, source_specs: list[SourceSpec]) -> Select:
    clauses = []

    for source_spec in source_specs:
        if source_spec.type == 'none': continue
        exists_stmt = exists_in_grouping(source_spec.type, Beatmap.id, source_spec.id)
        clauses.append(exists_stmt)

    if clauses:
        stmt = stmt.where(or_(*clauses))
    
    return stmt


def split_by_dash_or_none(value):
    if type(value) == str and '-' in value:
        return value.split('-')
    return None


def _get_filter_condition(stmt: Select, filter: Filter):
    field_column = filter_sort_fields.get_column__filter_field(field=filter.field, core_stmt=stmt)

    # print(filter)

    if field_column is None:
        return None

    match filter.field:
        case 'played_at':
            try:
                value = date_input_to_posix(filter.value)
            except ValueError as e:
                return None
        case 'ranked_date':
            try:
                value = date_input_to_posix(filter.value)
            except ValueError as e:
                return None
        case 'last_played_date':
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
        ## todo: because of this, equality for numbers does not work properly
        case '=':
            split_values = split_by_dash_or_none(filter.value)
            if split_values and len(split_values) == 2:
                return and_(field_column >= split_values[0], field_column < split_values[1])
            return field_column.ilike(f'%{value}%')


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
