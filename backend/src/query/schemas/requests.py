from typing import Literal
from pydantic import BaseModel

from .specs import CoreSpecs, PresentationSpecs


class BeatmapQueryRequest(BaseModel):
    core_specs: CoreSpecs
    presentation_specs: PresentationSpecs


class BeatmapQueryResult(BaseModel):
    beatmap_db_id: int
    beatmap_id: int
    beatmap_set_id: int
    md5_hash: str
    mode: int
    bpm: float
    difficulty_name: str
    ranked_status: int
    num_hitcircles: int
    num_sliders: int
    num_spinners: int
    approach_rate: float
    overall_difficulty: float
    circle_size: float
    hp_drain: float
    last_played: int
    drain_time: int
    total_time: int
    local_offset: int

    artist: str
    title: str
    owner: str
    song_source: str
    song_tags: str
