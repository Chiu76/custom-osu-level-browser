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
    pass


class ScoreQueryRow(BaseModel):
    pass


class ScoreQueryResponse(BaseModel):
    pass
