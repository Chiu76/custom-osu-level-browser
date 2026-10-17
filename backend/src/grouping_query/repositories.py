from sqlalchemy import Select, Subquery, select, func, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.beatmaps import Beatmap
from src.common.models.collections import Collection

from .schemas import GroupingQueryRequest, GroupingQueryRow
from .enums import GroupingTypeEnum

from .yyy_field_groupings import get_artist_grouping_sq, get_overall_difficulty_grouping_sq

import src.grouping_query.zzz_aggregated_count as zzz_aggregated_count


class GroupingQueryRepository:
    @classmethod
    async def query(cls, request: GroupingQueryRequest, session: AsyncSession) -> list[GroupingQueryRow]:
        grouping_query_stmt = cls.get_grouping_query_stmt(request)
        
        # from src.common.db import engine
        # print(grouping_query_stmt.compile(engine))

        results = session.execute(grouping_query_stmt).mappings().all()
        
        return [GroupingQueryRow.model_validate(result) for result in results]


    @classmethod
    def get_grouping_query_stmt(cls, request: GroupingQueryRequest) -> Select:
        aggregated_count_sq = zzz_aggregated_count.get_aggregated_count_sq(request)

        if request.grouping_type == GroupingTypeEnum.COLLECTIONS:
            grouping_query_stmt = cls.get_grouping_query_stmt__collection(aggregated_count_sq, request)
        elif request.grouping_type == GroupingTypeEnum.ARTIST:
            grouping_query_stmt = cls.get_grouping_query_stmt__artist(aggregated_count_sq, request)
        elif request.grouping_type == GroupingTypeEnum.OVERALL_DIFFICULTY:
            grouping_query_stmt = cls.get_grouping_query_stmt__overall_difficulty(aggregated_count_sq, request)

        return grouping_query_stmt


    @staticmethod
    def get_grouping_query_stmt__collection(aggregated_count_sq: Subquery, request: GroupingQueryRequest) -> Select:
        return (
            select(
                func.coalesce(request.grouping_type, request.grouping_type).label('grouping_type'),
                Collection.id.label('grouping_id'), 
                Collection.name.label('grouping_name'), 
                func.coalesce(aggregated_count_sq.c.total_count, 0).label('total_count'), 
                func.coalesce(aggregated_count_sq.c.selected_count, 0).label('selected_count'),
            )
            .select_from(Collection)
            .outerjoin(aggregated_count_sq, aggregated_count_sq.c.grouping_id == Collection.id)
            .where(Collection.name.ilike(f'%{request.q}%'))
        )


    @staticmethod
    def get_grouping_query_stmt__artist(aggregated_count_sq: Subquery, request: GroupingQueryRequest) -> Select:
        artist_grouping_sq = get_artist_grouping_sq()
        first_char = func.substr(func.lower(artist_grouping_sq.c.artist), 1, 1).label('first_char')
        
        return (
            select(
                func.coalesce(request.grouping_type, request.grouping_type).label('grouping_type'),
                artist_grouping_sq.c.grouping_id,
                first_char.label('grouping_name'),
                func.coalesce(aggregated_count_sq.c.total_count, 0).label('total_count'), 
                func.coalesce(aggregated_count_sq.c.selected_count, 0).label('selected_count'),
            )
            .select_from(artist_grouping_sq)
            .outerjoin(aggregated_count_sq, aggregated_count_sq.c.grouping_id == artist_grouping_sq.c.grouping_id)
            .group_by(first_char)
        )


    @staticmethod
    def get_grouping_query_stmt__overall_difficulty(aggregated_count_sq: Subquery, request: GroupingQueryRequest) -> Select:
        overall_difficulty_sq = get_overall_difficulty_grouping_sq()
        return (
            select(
                func.coalesce(request.grouping_type, request.grouping_type).label('grouping_type'),
                overall_difficulty_sq.c.grouping_id,
                overall_difficulty_sq.c.bins.label('grouping_name'),
                func.coalesce(aggregated_count_sq.c.total_count, 0).label('total_count'), 
                func.coalesce(aggregated_count_sq.c.selected_count, 0).label('selected_count'),
            )
            .select_from(overall_difficulty_sq)
            .outerjoin(aggregated_count_sq, aggregated_count_sq.c.grouping_id == overall_difficulty_sq.c.grouping_id)
            .group_by(overall_difficulty_sq.c.bins)
        )
