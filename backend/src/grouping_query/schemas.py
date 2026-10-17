from pydantic import BaseModel

from src.beatmap_query.schemas.requests import BeatmapQueryRequest
from .enums import GroupingType


class GroupingQueryRequest(BaseModel):
    beatmap_query_request: BeatmapQueryRequest
    grouping_type: GroupingType
    q: str
    

class GroupingQueryRow(BaseModel):
    grouping_type: GroupingType
    grouping_id: int
    grouping_name: str
    total_count: int
    selected_count: int


class GroupingQueryResponse(BaseModel):
    rows: list[GroupingQueryRow]
