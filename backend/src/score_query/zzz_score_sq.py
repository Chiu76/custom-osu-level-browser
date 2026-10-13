from sqlalchemy import Over, Select, Subquery, select, func, alias
from sqlalchemy.orm import Session, InstrumentedAttribute

from .schemas.specs import ScoreSqSpec
from .yyy_top_by import get_column__top_by
from .yyy_mods import apply_mods

from src.common.models.scores import Score


def get_score_sq(score_sq_spec: ScoreSqSpec) -> Subquery:
    score_row_num_sq = build_score_row_num_sq(score_sq_spec)
    score_sq = build_score_sq(score_row_num_sq, score_sq_spec)
    
    return score_sq


def build_score_row_num_sq(score_sq_spec: ScoreSqSpec) -> Subquery:
    column__top_by = get_column__top_by(score_sq_spec.top_by)
    column__top_by = column__top_by.desc() if score_sq_spec.top_by_desc else column__top_by

    score_row_num_sq = (
        select(
            Score.grade, 
            Score.accuracy,
            Score.played_at,
            Score.beatmap_db_id,
            _get_row_num_over(column__top_by).label('row_num'),
        )
    )

    score_row_num_sq = apply_mods(
        score_row_num_sq, 
        score_sq_spec.mods_exact, 
        score_sq_spec.mods_include, 
        score_sq_spec.mods_exclude
    )

    return score_row_num_sq.subquery('score_row_num_sq')


def build_score_sq(score_row_num_sq: Subquery, score_sq_spec: ScoreSqSpec) -> Subquery:
    score_sq = (
        select(*score_row_num_sq.c)
        .select_from(score_row_num_sq)
    )

    if score_sq_spec.top_score_only:
        score_sq = score_sq.where(score_row_num_sq.c.row_num == 1)

    return score_sq.subquery('score_sq')


def _get_row_num_over(column__top_by: InstrumentedAttribute) -> Over:
    return func.row_number().over(
        partition_by=Score.beatmap_db_id,
        order_by=column__top_by,
    )
