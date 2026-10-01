from typing import Literal
from pydantic import BaseModel


class NoneIdentifier(BaseModel):
    type: Literal['none']


class LocalBeatmapsIdentifier(BaseModel):
    type: Literal['local_beatmaps']
