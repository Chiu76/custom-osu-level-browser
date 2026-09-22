from typing import Literal, Annotated
from pydantic import BaseModel, Field

from .identifiers import NoneIdentifier, LocalBeatmapsIdentifier
from ..filter_sort_fields import FILTER_SORT_FIELD


SourceSpec = Annotated[
    LocalBeatmapsIdentifier, # | AllRankedBeatmapsIdentifier | TimeBasedBeatmapsIdentifier | PackIdentifier | CollectionIdentifier, 
    Field(discriminator='type')
]


class StarRatingSpec(BaseModel):
    pass


class AttachedScoreSpec(BaseModel):
    pass


class OnlineDetailsSpec(BaseModel):
    pass


class Filter(BaseModel):
    field: FILTER_SORT_FIELD
    op: Literal['!=', '<', '<=', '>', '>=', '=']
    value: int | float | str


class FilterSpec(BaseModel):
    filters: list[Filter] = []
	

class CoreSpecs(BaseModel):
    star_rating_spec: StarRatingSpec
    attached_score_spec: AttachedScoreSpec 
    online_details_spec: OnlineDetailsSpec
    source_spec: SourceSpec
    filter_spec: FilterSpec


class SearchSpec(BaseModel):
    q: str | None = None


GroupingSpec = Annotated[
    NoneIdentifier | LocalBeatmapsIdentifier, # | AllRankedBeatmapsIdentifier | TimeBasedBeatmapsIdentifier | PackIdentifier | CollectionIdentifier, 
    Field(discriminator='type')
]


class Sorting(BaseModel):
    field: FILTER_SORT_FIELD
    dir: Literal['asc', 'desc'] = 'asc'


class SortingSpec(BaseModel):
    sortings: list[Sorting] = []


class PresentationSpecs(BaseModel):
    search_spec: SearchSpec
    grouping_spec: GroupingSpec
    sorting_spec: SortingSpec
