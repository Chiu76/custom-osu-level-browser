from sqlalchemy import Boolean, Integer, Float, String, Unicode, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Model


class BeatmapSet(Model):
    __tablename__ = 'beatmap_sets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    beatmap_set_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    artist: Mapped[str] = mapped_column(String(255))
    artist_unicode: Mapped[str] = mapped_column(Unicode(255))
    title: Mapped[str] = mapped_column(String(255))
    title_unicode: Mapped[str] = mapped_column(Unicode(255))

    owner: Mapped[str] = mapped_column(String(255))

    song_source: Mapped[str] = mapped_column(String(255))
    song_tags: Mapped[str] = mapped_column(String)

    online_offset: Mapped[int] = mapped_column(Integer)
    is_osz2: Mapped[bool] = mapped_column(Boolean)

    folder_name: Mapped[str] = mapped_column(String(255))

    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    def __repr__(self):
        return f'BeatmapSet(beatmap_set_id={self.beatmap_set_id}, {self.artist} - {self.title} ({self.owner}))'


class Beatmap(Model):
    __tablename__ = 'beatmaps'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beatmap_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    beatmap_set_id: Mapped[int] = mapped_column(
        ForeignKey('beatmap_sets.beatmap_set_id', ondelete='CASCADE'),
        nullable=False,
    )

    md5_hash: Mapped[int] = mapped_column(String(32), unique=True, nullable=False, index=True)

    mode: Mapped[int] = mapped_column(Integer)
    bpm: Mapped[float] = mapped_column(Float)

    difficulty_name: Mapped[str] = mapped_column(String(255))

    audio_file: Mapped[str] = mapped_column(String(255))
    map_file: Mapped[str] = mapped_column(String(255))

    ranked_status: Mapped[int] = mapped_column(Integer)

    num_hitcircles: Mapped[int] = mapped_column(Integer)
    num_sliders: Mapped[int] = mapped_column(Integer)
    num_spinners: Mapped[int] = mapped_column(Integer)

    approach_rate: Mapped[int] = mapped_column(Float)
    overall_difficulty: Mapped[int] = mapped_column(Float)
    circle_size: Mapped[int] = mapped_column(Float)
    hp_drain: Mapped[int] = mapped_column(Float)

    last_played: Mapped[int] = mapped_column(Integer)
    last_modified: Mapped[int] = mapped_column(Integer)

    drain_time: Mapped[int] = mapped_column(Integer)
    total_time: Mapped[int] = mapped_column(Integer)

    local_offset: Mapped[int] = mapped_column(Integer)

    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    def __repr__(self):
        return f'Beatmap(beatmap_id={self.beatmap_id})'


class BeatmapStarRating(Model):
    __tablename__ = 'beatmap_star_rating'

    beatmap_db_id: Mapped[int] = mapped_column(
        ForeignKey('beatmaps.id', ondelete='CASCADE'),
        index=True,
        primary_key=True,
    )
    mode: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    mods: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    star_rating: Mapped[float] = mapped_column(Float)

    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
