from pydantic import BaseModel

from .identifiers import GroupingTypeIdentifier
from src.beatmap_query.schemas.requests import BeatmapQueryRequest


class GroupingQueryRequest(BaseModel):
    beatmap_query_request: BeatmapQueryRequest
    grouping_type: GroupingTypeIdentifier
    q: str
    

class GroupingQueryRow(BaseModel):
    id: int
    name: str
    total_count: int
    selected_count: int


class GroupingQueryResponse(BaseModel):
    rows: list[GroupingQueryRow]
    grouping_type: GroupingTypeIdentifier
