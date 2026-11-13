import json

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import BeatmapSet

import src.ingestion.tasks.zzz_common as task_common

from src.common.db import get_osu_api_data_cache_engine


def get_beatmap_set_mapping(beatmap_set_db_content: dict, import_source_hash: str) -> dict:
    return {
        'beatmap_set_id': beatmap_set_db_content['beatmaps'][0]['beatmapset_id'],
        'artist': beatmap_set_db_content['artist'],
        'artist_unicode': beatmap_set_db_content['artist_unicode'],
        'title': beatmap_set_db_content['title'],
        'title_unicode': beatmap_set_db_content['title_unicode'],
        'owner': beatmap_set_db_content['creator'],
        'song_source': beatmap_set_db_content['source'],
        'song_tags': beatmap_set_db_content['tags'],
        'online_offset': beatmap_set_db_content['offset'],
        'is_osz2': True,
        'folder_name': '',
        'import_source_hash': import_source_hash,
    }


def get_osu_api_data_cache__beatmapsets():
    engine = get_osu_api_data_cache_engine()
    with engine.connect() as conn:
        results = conn.execute(
            text('''
            SELECT id, content 
            FROM beatmap_sets;
            ''')
        ).mappings().all()
    return results


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

    osu_db_file_hash = utils.get_state__db_file_hash('osu!', session)
    beatmap_set_data = get_osu_api_data_cache__beatmapsets()

    beatmap_set_rows = []
    for beatmap_set in beatmap_set_data:
        row = get_beatmap_set_mapping(
            beatmap_set_db_content=json.loads(beatmap_set['content']),
            import_source_hash=osu_db_file_hash,
        )
        beatmap_set_rows.append(row)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(BeatmapSet)
        .where(BeatmapSet.import_source_hash == osu_db_file_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(beatmap_set_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=beatmap_set_rows,
            target_table=BeatmapSet,
            table_unique_keys=['beatmap_set_id'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_beatmap_sets_advanced(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_beatmap_sets_advanced',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
