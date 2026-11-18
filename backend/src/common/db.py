import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Model(DeclarativeBase):
    metadata = MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })


load_dotenv()
 
engine = create_engine(
    url="sqlite:///db.sqlite",
    echo=False,
)

SessionMaker = sessionmaker(engine)


def get_osu_api_data_cache_engine():
    url = f'sqlite:///{os.environ["OSU_API_DATA_CACHE_DB_PATH"]}'
    return create_engine(
        url=url,
        echo=False,
    )
