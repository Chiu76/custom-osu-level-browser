from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Model


class Collection(Model):
    __tablename__ = 'collections'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)


class CollectionItem(Model):
    __tablename__ = 'collection_items'

    collection_id: Mapped[int] = mapped_column(
        ForeignKey('collections.id', ondelete='CASCADE'),
        primary_key=True,
        index=True,
    )

    beatmap_db_id: Mapped[int] = mapped_column(
        ForeignKey('beatmaps.id', ondelete='CASCADE'),
        primary_key=True,
    )

    md5_hash: Mapped[int] = mapped_column(String(32), nullable=False, index=True)

    import_source_hash: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
