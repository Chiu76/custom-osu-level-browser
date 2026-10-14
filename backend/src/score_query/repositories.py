from sqlalchemy import Select, Subquery, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.scores import Score

from .schemas import ScoreQueryRequest, ScoreQueryRow

from .zzz_score_sq import get_score_sq


class ScoreQueryRepository:
    @classmethod
    async def query(cls, request: ScoreQueryRequest, session: AsyncSession) -> list[ScoreQueryRow]:
        score_query_stmt = cls.get_score_query_stmt(request)
        
        results = session.execute(score_query_stmt).mappings().all()
        
        return [ScoreQueryRow.model_validate(result) for result in results]


    @classmethod
    def get_score_query_stmt(cls, request: ScoreQueryRequest) -> Select:
        score_sq = get_score_sq(request.score_sq_spec)
        score_query_stmt = (
            select(*score_sq.c)
            .select_from(score_sq)
            .where(score_sq.c.beatmap_db_id == request.beatmap_db_id)
        )
        return score_query_stmt
