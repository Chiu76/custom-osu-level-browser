from typing import Literal
from enum import StrEnum

GroupingType = Literal[
    'collections',
    'packs',
    'artist',
    'overall_difficulty',
    'ranked_year',
    'ranked_month',
]

class GroupingTypeEnum(StrEnum):
    COLLECTIONS = 'collections',
    PACKS = 'packs',
    ARTIST = 'artist',
    OVERALL_DIFFICULTY = 'overall_difficulty',
    RANKED_YEAR = 'ranked_year',
    RANKED_MONTH = 'ranked_month',