from sqlalchemy import Over, Select, Subquery, select, func, alias
from sqlalchemy.orm import Session, InstrumentedAttribute

from .schemas.requests import ScoreQueryRequest

from src.common.models.scores import Score


def _get_row_num_over(top_by: InstrumentedAttribute) -> Over:
    return func.row_number().over(
        partition_by=Score.beatmap_db_id,
        order_by=Score.accuracy,
    )


def get_scores_sq(request: ScoreQueryRequest = None) -> Subquery:
    scores_row_num_sq = (
        select(
            Score.grade, 
            Score.accuracy, 
            Score.beatmap_db_id, 
            _get_row_num_over(Score.accuracy).label('row_num'),
        )
        .subquery('scores_row_num_sq')
    )

    scores_sq = (
        select(
            scores_row_num_sq.c.grade,
            scores_row_num_sq.c.accuracy,
            scores_row_num_sq.c.beatmap_db_id,
            ## todo: delete row_num from query
            scores_row_num_sq.c.row_num,
        )
        .select_from(scores_row_num_sq)
        .where(scores_row_num_sq.c.row_num == 1)
        .subquery('scores_sq')
    )
    
    return scores_sq