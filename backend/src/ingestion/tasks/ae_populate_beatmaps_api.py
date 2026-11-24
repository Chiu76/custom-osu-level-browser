import json

from sqlalchemy import select, func, text, distinct
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap

import src.ingestion.tasks.zzz_common as task_common

from src.common.db import get_osu_api_data_cache_engine


def get_beatmap_mapping(beatmap_db_content: dict, import_source_hash: str) -> dict:
    return {
        'beatmap_id': beatmap_db_content['id'],
        'beatmapset_id': beatmap_db_content['beatmapset_id'],
        'md5_hash': beatmap_db_content['checksum'],
        'mode': beatmap_db_content['mode'],
        'bpm': beatmap_db_content['bpm'],
        'difficulty_name': beatmap_db_content['version'],
        'ranked_status': beatmap_db_content['status'],
        'num_hitcircles': beatmap_db_content['count_circles'],
        'num_sliders': beatmap_db_content['count_sliders'],
        'num_spinners': beatmap_db_content['count_spinners'],
        'approach_rate': beatmap_db_content['ar'],
        'overall_difficulty': beatmap_db_content['accuracy'],
        'circle_size': beatmap_db_content['cs'],
        'hp_drain': beatmap_db_content['drain'],
        'drain_time': beatmap_db_content['hit_length'],
        'total_time': beatmap_db_content['total_length'],
        
        'creator_id': beatmap_db_content['user_id'],
        'creators': json.dumps(beatmap_db_content['owners']),
        'max_combo': beatmap_db_content['max_combo'],
        'play_count': beatmap_db_content['play_count'],
        'pass_count': beatmap_db_content['passcount'],
        'lazer_only': beatmap_db_content['lazer_only'],
        
        'import_type': 'API_DATA',
        'import_source_hash': import_source_hash,
    }


def get_already_populated_beatmap_ids(session: Session) -> set:
    stmt_select_beatmap_ids = select(distinct(Beatmap.beatmap_id))
    return set(session.scalars(stmt_select_beatmap_ids).all())


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

    already_populated_beatmap_ids = get_already_populated_beatmap_ids(session)

    print(f'{len(already_populated_beatmap_ids)=}')

    beatmap_rows = []
    for beatmapset in beatmapset_data:
        for beatmap_content in json.loads(beatmapset['content'])['beatmaps']:
            beatmap_id = int(beatmap_content['id'])
            if beatmap_id in already_populated_beatmap_ids: continue
            ## todo: hardcoded osu!std only section
            if beatmap_content['mode'] != 0: continue
            row = get_beatmap_mapping(
                beatmap_db_content=beatmap_content, 
                import_source_hash=beatmapset_data_hash,
            )
            beatmap_rows.append(row)

    print(f'{len(beatmap_rows)=}')

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Beatmap)
        .where(Beatmap.import_source_hash == beatmapset_data_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(beatmap_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=beatmap_rows,
            target_table=Beatmap,
            table_unique_keys=['beatmap_id'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_beatmaps_api(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_beatmaps_api',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
