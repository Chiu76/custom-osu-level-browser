import json

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

from src.common.db import get_osu_api_data_cache_engine
from src.common.models.beatmaps import Beatmapset
import src.common.utils as utils

import src.ingestion.tasks.zzz_common as task_common


def get_beatmapset_mapping(beatmapset_db_content: dict, import_source_hash: str) -> dict:
    return {
        'beatmapset_id': beatmapset_db_content['beatmaps'][0]['beatmapset_id'],
        'artist': beatmapset_db_content['artist'],
        'artist_unicode': beatmapset_db_content['artist_unicode'],
        'title': beatmapset_db_content['title'],
        'title_unicode': beatmapset_db_content['title_unicode'],
        'song_source': beatmapset_db_content['source'],
        'song_tags': beatmapset_db_content['tags'],
        'owner': beatmapset_db_content['creator'],
        
        'owner_id': beatmapset_db_content['user_id'],
        'play_count': beatmapset_db_content['play_count'],
        'favourite_count': beatmapset_db_content['favourite_count'],
        'rating': beatmapset_db_content['rating'],
        'genre_id': beatmapset_db_content['genre_id'],
        'language_id': beatmapset_db_content['language_id'],
        'spotlight': beatmapset_db_content['spotlight'],
        'submitted_date': task_common.osu_api_timestamp_to_posix(beatmapset_db_content['submitted_date']),
        'ranked_date': task_common.osu_api_timestamp_to_posix(beatmapset_db_content['ranked_date']),
        'ranked_year': task_common.osu_api_timestamp_to_year(beatmapset_db_content['ranked_date']),
        'ranked_month': task_common.osu_api_timestamp_to_month(beatmapset_db_content['ranked_date']),
        
        'import_type': 'API_DATA',
        'import_source_hash': import_source_hash,
    }


def get_osu_api_data_cache__beatmapsets():
    engine = get_osu_api_data_cache_engine()
    with engine.connect() as conn:
        results = conn.execute(
            text('''
            SELECT beatmapset_id, content 
            FROM beatmapsets;
            ''')
        ).mappings().all()
    return [dict(row) for row in results]


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}
    
def fn(self: Task, session: Session, force_refresh: bool = False):
    self.log_info('start_task')

    self.vars = {
        'to_import_items': None,
        'did_import_items': None,
        'num_items_to_import': None,
        'num_items_did_import': None,
        'failed_imports': None,
        'force_refresh': None,
    }

    beatmapset_data = get_osu_api_data_cache__beatmapsets()
    beatmapset_data_hash = utils.md5_hash_dict(beatmapset_data)

    beatmapset_rows = []
    for beatmapset in beatmapset_data:
        had_a_std_beatmap = False
        for beatmap in json.loads(beatmapset['content'])['beatmaps']:
            if beatmap['mode'] == 0: had_a_std_beatmap = True
        if had_a_std_beatmap:
            row = get_beatmapset_mapping(
                beatmapset_db_content=json.loads(beatmapset['content']),
                import_source_hash=beatmapset_data_hash,
            )
            beatmapset_rows.append(row)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Beatmapset)
        .where(Beatmapset.import_source_hash == beatmapset_data_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(beatmapset_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=beatmapset_rows,
            target_table=Beatmapset,
            table_unique_keys=['beatmapset_id'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_beatmapsets_api(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_beatmapsets_api',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
