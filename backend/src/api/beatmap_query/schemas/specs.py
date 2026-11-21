from typing import Literal, Annotated
from pydantic import BaseModel, Field

from .identifiers import NoneIdentifier, LocalBeatmapsIdentifier, GroupingIdentifier
from ..yyy_filter_sort_fields import FILTER_SORT_FIELDS, FILTER_SORT_FIELDS_ALTERNATIVES, FILTER_OPS

from src.api.score_query.schemas import ScoreSqSpec
from src.api.score_query.yyy_mods import MODS_FIELDS, MODS_FIELDS_ALTERNATIVES


SourceSpec = Annotated[
    NoneIdentifier | LocalBeatmapsIdentifier | GroupingIdentifier, # | AllRankedBeatmapsIdentifier | TimeBasedBeatmapsIdentifier | PackIdentifier,
    Field(discriminator='type')
]


class StarRatingSpec(BaseModel):
    mods: list[MODS_FIELDS | MODS_FIELDS_ALTERNATIVES]


class AttachedScoreSpec(BaseModel):
    score_sq_spec: ScoreSqSpec
    score_required: bool = False


class Filter(BaseModel):
    field: FILTER_SORT_FIELDS | FILTER_SORT_FIELDS_ALTERNATIVES
    op: FILTER_OPS
    value: int | float | str


class FilterSpec(BaseModel):
    filters: list[Filter] = []
	

class CoreSpecs(BaseModel):
    star_rating_spec: StarRatingSpec
    attached_score_spec: AttachedScoreSpec 
    source_specs: list[SourceSpec]
    filter_spec: FilterSpec


class SearchSpec(BaseModel):
    queries: list[str] = []


GroupingSpec = Annotated[
    NoneIdentifier | LocalBeatmapsIdentifier | GroupingIdentifier, # | AllRankedBeatmapIdentifier | TemporalBeatmapIdentifier | PackIdentifier, 
    Field(discriminator='type')
]


class Sort(BaseModel):
    field: FILTER_SORT_FIELDS | FILTER_SORT_FIELDS_ALTERNATIVES
    dir: Literal['asc', 'desc'] = 'asc'


class SortSpec(BaseModel):
    sort_columns: list[Sort] = []


class PresentationSpecs(BaseModel):
    search_spec: SearchSpec
    grouping_specs: list[GroupingSpec]
    sort_spec: SortSpec
