from pydantic import BaseModel

from src.api.beatmap_query.schemas.requests import BeatmapQueryRequest
from .yyy_field_groupings import GroupingType


class GroupingQueryRequest(BaseModel):
    beatmap_query_request: BeatmapQueryRequest
    grouping_type: GroupingType
    q: str
    show_selected_counts: bool
    

class GroupingQueryRow(BaseModel):
    grouping_type: GroupingType
    grouping_id: int
    grouping_name: str
    total_count: int
    selected_count: int


class GroupingQueryResponse(BaseModel):
    rows: list[GroupingQueryRow]
