from pydantic import BaseModel

from ..yyy_top_by import TOP_BY
from ..yyy_mods import MODS, MODS_ALTERNATIVES


class ScoreSqSpec(BaseModel):
    top_by: TOP_BY
    top_by_desc: bool = False
    top_score_only: bool = True
    mods_exact: list[MODS | MODS_ALTERNATIVES] = []
    mods_include: list[MODS | MODS_ALTERNATIVES] = []
    mods_exclude: list[MODS | MODS_ALTERNATIVES] = []