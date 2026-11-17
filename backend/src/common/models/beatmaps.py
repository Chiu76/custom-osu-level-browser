from typing import Optional

from sqlalchemy import Boolean, Integer, Float, String, Unicode, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Model


class Beatmapset(Model):
    __tablename__ = 'beatmapsets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    beatmapset_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    artist: Mapped[str] = mapped_column(String(255))
    artist_unicode: Mapped[str] = mapped_column(Unicode(255))
    title: Mapped[str] = mapped_column(String(255))
    title_unicode: Mapped[str] = mapped_column(Unicode(255))

    song_source: Mapped[str] = mapped_column(String(255))
    song_tags: Mapped[str] = mapped_column(String)

    owner: Mapped[str] = mapped_column(String(255))

    # API import fields
    owner_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    play_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    favourite_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    genre_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    spotlight: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    submitted_date: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ranked_date: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    deleted_date: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # import details fields
    import_type: Mapped[str] = mapped_column(String(32), nullable=False)
    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)


class Beatmap(Model):
    __tablename__ = 'beatmaps'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    beatmap_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    beatmapset_id: Mapped[int] = mapped_column(
        ForeignKey('beatmapsets.beatmapset_id', ondelete='CASCADE'),
        nullable=False,
    )

    md5_hash: Mapped[int] = mapped_column(String(32), unique=True, nullable=False, index=True)

    mode: Mapped[int] = mapped_column(Integer)
    bpm: Mapped[float] = mapped_column(Float)

    difficulty_name: Mapped[str] = mapped_column(String(255))

    ranked_status: Mapped[int] = mapped_column(Integer)

    num_hitcircles: Mapped[int] = mapped_column(Integer)
    num_sliders: Mapped[int] = mapped_column(Integer)
    num_spinners: Mapped[int] = mapped_column(Integer)

    approach_rate: Mapped[int] = mapped_column(Float)
    overall_difficulty: Mapped[int] = mapped_column(Float)
    circle_size: Mapped[int] = mapped_column(Float)
    hp_drain: Mapped[int] = mapped_column(Float)

    drain_time: Mapped[int] = mapped_column(Integer)
    total_time: Mapped[int] = mapped_column(Integer)

    # API import fields
    creator_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    creators: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    max_combo: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    play_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    pass_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    lazer_only: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    deleted_date: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # osu!stable import fields
    last_played_date: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # import details fields
    import_type: Mapped[str] = mapped_column(String(32), nullable=False)
    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)


class BeatmapStarRating(Model):
    __tablename__ = 'beatmaps_star_ratings'

    beatmap_db_id: Mapped[int] = mapped_column(
        ForeignKey('beatmaps.id', ondelete='CASCADE'),
        index=True,
        primary_key=True,
    )
    
    mode: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    mods: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    
    star_rating: Mapped[float] = mapped_column(Float, index=True)
    star_rating_aim: Mapped[Optional[float]] = mapped_column(Float, nullable=True, index=True)
    star_rating_speed: Mapped[Optional[float]] = mapped_column(Float, nullable=True, index=True)
    star_rating_reading: Mapped[Optional[float]] = mapped_column(Float, nullable=True, index=True)

    import_type: Mapped[str] = mapped_column(String(32), nullable=False)
    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
