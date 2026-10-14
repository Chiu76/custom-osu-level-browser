from typing import Literal, Annotated
from pydantic import BaseModel, Field

from .identifiers import NoneIdentifier, LocalBeatmapsIdentifier, CollectionsIdentifier
from ..yyy_filter_sort_fields import FILTER_SORT_FIELDS, FILTER_SORT_FIELDS_ALTERNATIVES, FILTER_OPS

from src.score_query.schemas import ScoreSqSpec


SourceSpec = Annotated[
    LocalBeatmapsIdentifier | CollectionsIdentifier, # | AllRankedBeatmapsIdentifier | TimeBasedBeatmapsIdentifier | PackIdentifier,
    Field(discriminator='type')
]


class StarRatingSpec(BaseModel):
    pass


class AttachedScoreSpec(BaseModel):
    score_sq_spec: ScoreSqSpec
    score_required: bool = False


class OnlineDetailsSpec(BaseModel):
    pass


class Filter(BaseModel):
    field: FILTER_SORT_FIELDS | FILTER_SORT_FIELDS_ALTERNATIVES
    op: FILTER_OPS
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
    NoneIdentifier | LocalBeatmapsIdentifier | CollectionsIdentifier, # | AllRankedBeatmapsIdentifier | TemporalBeatmapsIdentifier | PackIdentifier, 
    Field(discriminator='type')
]


class Sort(BaseModel):
    field: FILTER_SORT_FIELDS | FILTER_SORT_FIELDS_ALTERNATIVES
    dir: Literal['asc', 'desc'] = 'asc'


class SortSpec(BaseModel):
    sort_columns: list[Sort] = []


class PresentationSpecs(BaseModel):
    search_spec: SearchSpec
    grouping_spec: GroupingSpec
    sort_spec: SortSpec
