from typing import Literal

from pydantic import BaseModel

from src.api.grouping_query.yyy_field_groupings import GroupingType


class NoneIdentifier(BaseModel):
    type: Literal['none']


class GroupingIdentifier(BaseModel):
    type: Literal[GroupingType]
    id: int
