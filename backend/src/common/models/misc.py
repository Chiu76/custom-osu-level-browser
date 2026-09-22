from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Model


class State(Model):
    __tablename__ = 'state'

    id: Mapped[int] = mapped_column(primary_key=True)

    osu_db_file_hash: Mapped[str] = mapped_column(String(32), nullable=False)

    def __repr__(self):
        return f'State({self.osu_db_file_hash=})'
