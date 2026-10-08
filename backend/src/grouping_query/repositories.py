from sqlalchemy import Select, Subquery, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.collections import Collection

from .schemas.identifiers import GroupingTypeIdentifier
from .schemas.requests import GroupingQueryRequest, GroupingQueryRow

import src.grouping_query.zzz_aggregated_count as zzz_aggregated_count


class GroupingQueryRepository:
    @classmethod
    async def query(cls, request: GroupingQueryRequest, session: AsyncSession) -> GroupingQueryRow:
        grouping_query_stmt = cls.get_grouping_query_stmt(request)

        results = session.execute(grouping_query_stmt).mappings().all()
        
        return [GroupingQueryRow.model_validate(result) for result in results]


    @classmethod
    def get_grouping_query_stmt(cls, request: GroupingQueryRequest) -> Select:
        aggregated_count_sq = zzz_aggregated_count.get_aggregated_count_sq(request)

        if request.grouping_type == GroupingTypeIdentifier.COLLECTIONS:
            grouping_query_stmt = cls.get_grouping_query_stmt__collection(aggregated_count_sq, request.q)    
        
        return grouping_query_stmt


    @staticmethod
    def get_grouping_query_stmt__collection(aggregated_count_sq: Subquery, q: str) -> Select:
        return (
            select(
                Collection.id.label('collection_id'), 
                Collection.name.label('name'), 
                aggregated_count_sq.c.total_count, 
                aggregated_count_sq.c.selected_count,
            )
            .select_from(Collection)
            .join(aggregated_count_sq, aggregated_count_sq.c.grouping_id == Collection.id)
            .where(Collection.name.ilike(f'%{q}%'))
        )
