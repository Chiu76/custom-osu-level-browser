from sqlalchemy import select, func
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmapset

import src.ingestion.tasks.zzz_common as task_common


def get_beatmapset_mapping(beatmap_db_content: dict, import_source_hash: str) -> dict:
    return {
        'beatmapset_id': beatmap_db_content['beatmap_set_id'],
        'artist': beatmap_db_content['artist'],
        'artist_unicode': beatmap_db_content['artist_unicode'],
        'title': beatmap_db_content['title'],
        'title_unicode': beatmap_db_content['title_unicode'],
        'owner': beatmap_db_content['mapper'],
        'song_source': beatmap_db_content['song_source'],
        'song_tags': beatmap_db_content['song_tags'],
        'import_type': 'STABLE_LOCAL_DATA',
        'import_source_hash': import_source_hash,
    }


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
    beatmap_data = utils.load_json__db_file("osu!", osu_db_file_hash)['beatmap_data']

    set_ids = set()
    beatmapset_rows = []
    for beatmap in beatmap_data:
        set_id = beatmap['beatmap_set_id']
        if set_id in set_ids: continue
        mapping = get_beatmapset_mapping(beatmap, import_source_hash=osu_db_file_hash)
        beatmapset_rows.append(mapping)
        set_ids.add(set_id)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Beatmapset)
        .where(Beatmapset.import_source_hash == osu_db_file_hash)
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


def init_task__populate_beatmapsets(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_beatmapsets',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
