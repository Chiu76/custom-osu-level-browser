from pydantic import BaseModel

from src.beatmap_query.schemas.requests import BeatmapQueryRequest


class ScoreQueryRequest(BaseModel):
    beatmap_query_request: BeatmapQueryRequest
    q: str
    

class ScoreQueryRow(BaseModel):
    id: int
    name: str
    total_count: int
    selected_count: int


class ScoreQueryResponse(BaseModel):
    rows: list[ScoreQueryRow]
