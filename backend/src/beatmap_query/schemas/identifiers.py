from typing import Literal
from enum import StrEnum

from pydantic import BaseModel


class NoneIdentifier(BaseModel):
    type: Literal['none']


class LocalBeatmapsIdentifier(BaseModel):
    type: Literal['local_beatmaps']


class CollectionIdentifier(BaseModel):
    type: Literal['collection']
    id: int
