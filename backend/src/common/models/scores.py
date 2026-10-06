from sqlalchemy import Boolean, Integer, BigInteger, Float, String, Unicode, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Model


# class Score(Model):
#     __tablename__ = 'scores'

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)

#     beatmap_db_id: Mapped[int] = mapped_column(
#         ForeignKey('beatmaps.id', ondelete='CASCADE'),
#         nullable=False,
#     )