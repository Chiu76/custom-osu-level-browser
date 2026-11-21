from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import GroupingQueryRequest, GroupingQueryRow

import src.api.grouping_query.zzz_grouping_query as zzz_grouping_query


class GroupingQueryRepository:
    @classmethod
    async def query(cls, request: GroupingQueryRequest, session: AsyncSession) -> list[GroupingQueryRow]:
        grouping_query_stmt = zzz_grouping_query.get_grouping_query_stmt(request)

        results = session.execute(grouping_query_stmt).mappings().all()
        
        return [GroupingQueryRow.model_validate(result) for result in results]
