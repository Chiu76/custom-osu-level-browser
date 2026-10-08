from pydantic import BaseModel

from .identifiers import GroupingTypeIdentifier
from src.beatmap_query.schemas.requests import BeatmapQueryRequest


class GroupingQueryRequest(BaseModel):
    beatmap_query_request: BeatmapQueryRequest
    type: GroupingTypeIdentifier
    q: str
    

class GroupingQueryRow(BaseModel):
    grouping_id: int
    name: str
    total_count: int
    selected_count: int


class GroupingQueryResponse(BaseModel):
    rows: list[GroupingQueryRow]
    type: GroupingTypeIdentifier
