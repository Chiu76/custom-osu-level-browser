from typing import Literal
from pydantic import BaseModel

from .yyy_top_by_fields import TOP_BY_FIELDS
from .yyy_mods import MODS_FIELDS, MODS_FIELDS_ALTERNATIVES


class TopBy(BaseModel):
    field: TOP_BY_FIELDS
    dir: Literal['asc', 'desc'] = 'desc'


class ScoreSqSpec(BaseModel):
    top_by: TopBy
    top_score_only: bool = True
    mods_exact: list[MODS_FIELDS | MODS_FIELDS_ALTERNATIVES] = []
    mods_include: list[MODS_FIELDS | MODS_FIELDS_ALTERNATIVES] = []
    mods_exclude: list[MODS_FIELDS | MODS_FIELDS_ALTERNATIVES] = []


class ScoreQueryRequest(BaseModel):
    score_sq_spec: ScoreSqSpec
    beatmap_db_id: int


class ScoreQueryRow(BaseModel):
    mode: int
    player_name: str
    num_300s: int
    num_100s: int
    num_50s: int
    num_gekis: int
    num_katus: int
    num_misses: int
    grade: str
    accuracy: float
    replay_score: int
    max_combo: int
    perfect_combo: bool
    mods: int
    played_at: int


class ScoreQueryResponse(BaseModel):
    rows: list[ScoreQueryRow]
    count: int
