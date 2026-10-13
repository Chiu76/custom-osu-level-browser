from pydantic import BaseModel

from .enums import GroupingType
from src.beatmap_query.schemas.requests import BeatmapQueryRequest


class GroupingQueryRequest(BaseModel):
    beatmap_query_request: BeatmapQueryRequest
    grouping_type: GroupingType
    q: str
    

class GroupingQueryRow(BaseModel):
    id: int
    name: str
    total_count: int
    selected_count: int


class GroupingQueryResponse(BaseModel):
    rows: list[GroupingQueryRow]
    grouping_type: GroupingType
