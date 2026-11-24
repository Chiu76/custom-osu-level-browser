from typing import Optional

from sqlalchemy import UniqueConstraint, Boolean, Integer, BigInteger, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Model


class Score(Model):
    __tablename__ = 'scores'

    __table_args__ = (
        UniqueConstraint('beatmap_db_id', 'player_id', 'mode', 'mods', 'replay_score'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    beatmap_db_id: Mapped[int] = mapped_column(
        ForeignKey('beatmaps.id', ondelete='CASCADE'),
        nullable=False,
    )

    online_score_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    player_id: Mapped[int] = mapped_column(Integer, nullable=False)

    mode: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    mods: Mapped[int] = mapped_column(Integer, nullable=False)

    num_300s: Mapped[int] = mapped_column(Integer, nullable=False)
    num_100s: Mapped[int] = mapped_column(Integer, nullable=False)
    num_50s: Mapped[int] = mapped_column(Integer, nullable=False)
    num_gekis: Mapped[int] = mapped_column(Integer, nullable=False)
    num_katus: Mapped[int] = mapped_column(Integer, nullable=False)
    num_misses: Mapped[int] = mapped_column(Integer, nullable=False)

    grade: Mapped[str] = mapped_column(String(4), nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, nullable=False)

    replay_score: Mapped[int] = mapped_column(Integer, nullable=False)

    max_combo: Mapped[int] = mapped_column(Integer, nullable=False)
    perfect_combo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    played_at: Mapped[int] = mapped_column(Integer, nullable=False)

    # API import fields
    passed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    pp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # osu!stable import fields
    player_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    beatmap_md5_hash: Mapped[Optional[int]] = mapped_column(String(32), nullable=True)
    replay_md5_hash: Mapped[Optional[int]] = mapped_column(String(32), nullable=True)

    # import details fields
    import_type: Mapped[str] = mapped_column(String(32), nullable=False)
    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
