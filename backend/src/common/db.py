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
DATABASE_URL = ''

engine = create_engine(
    url=os.environ['DATABASE_URL'],
    echo=False,
)

SessionMaker = sessionmaker(engine)

def access_osu_api_data_cache():
    engine = create_engine(
        url=os.environ['OSU_API_DATA_CACHE_DATABASE_URL'],
    )
    with engine.connect() as conn:
        results = conn.execute(
            text('''
                SELECT tag, coalesce(ruleset_id, 0) as mode, beatmap_set_ids 
                FROM beatmap_packs
                ORDER BY tag
            ''')
            # text('SELECT count(*) FROM beatmap_packs')
        ).mappings().all()
        # print(results)
        return results[:5]
