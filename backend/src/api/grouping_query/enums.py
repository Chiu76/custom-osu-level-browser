from typing import Literal
from enum import StrEnum

GroupingType = Literal[
    'collections',
    'artist',
    'overall_difficulty',
    'ranked_year',
]

class GroupingTypeEnum(StrEnum):
    COLLECTIONS = 'collections',
    ARTIST = 'artist',
    OVERALL_DIFFICULTY = 'overall_difficulty',
    RANKED_YEAR = 'ranked_year',