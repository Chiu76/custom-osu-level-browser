from typing import Optional

from sqlalchemy import UniqueConstraint, Boolean, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Model


class Score(Model):
    __tablename__ = 'scores'

    __table_args__ = (
        UniqueConstraint('beatmap_md5_hash', 'replay_md5_hash'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    beatmap_db_id: Mapped[int] = mapped_column(
        ForeignKey('beatmaps.id', ondelete='CASCADE'),
        nullable=False,
    )

    mode: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)

    player_name: Mapped[str] = mapped_column(String(255), nullable=False)

    beatmap_md5_hash: Mapped[int] = mapped_column(String(32), nullable=False, index=True)
    replay_md5_hash: Mapped[int] = mapped_column(String(32), nullable=False, index=True)

    num_300s: Mapped[int] = mapped_column(Integer, nullable=False)
    num_100s: Mapped[int] = mapped_column(Integer, nullable=False)
    num_50s: Mapped[int] = mapped_column(Integer, nullable=False)
    num_gekis: Mapped[int] = mapped_column(Integer, nullable=False)
    num_katus: Mapped[int] = mapped_column(Integer, nullable=False)
    num_misses: Mapped[int] = mapped_column(Integer, nullable=False)

    grade: Mapped[str] = mapped_column(String(4), nullable=False)

    replay_score: Mapped[int] = mapped_column(Integer, nullable=False)

    max_combo: Mapped[int] = mapped_column(Integer, nullable=False)
    perfect_combo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    mods: Mapped[int] = mapped_column(Integer, nullable=False)

    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)

    online_score_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
