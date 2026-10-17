from typing import Literal
from enum import StrEnum

from pydantic import BaseModel

from src.grouping_query.enums import GroupingType


class NoneIdentifier(BaseModel):
    type: Literal['none']


class LocalBeatmapsIdentifier(BaseModel):
    type: Literal['local_beatmaps']


class GroupingIdentifier(BaseModel):
    type: Literal[GroupingType]
    id: int
