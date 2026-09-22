import json

from sqlalchemy import select, func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap

import src.ingestion.tasks.zzz_common as task_common


def compute_bpm(timing_points: dict) -> float:
    return 67


def get_table_row__beatmaps(beatmap_db_content: dict, import_source_hash: str) -> dict:
    return {
        'beatmap_set_id': beatmap_db_content['beatmap_set_id'],
        'beatmap_id': beatmap_db_content['beatmap_id'],
        'md5_hash': beatmap_db_content['md5_hash'],
        'mode': beatmap_db_content['gameplay_mode'],
        'difficulty_name': beatmap_db_content['difficulty'],
        'bpm': compute_bpm(beatmap_db_content['timing_points']),
        'audio_file': beatmap_db_content['audio_file'],
        'map_file': beatmap_db_content['map_file'],
        'ranked_status': beatmap_db_content['ranked_status'],
        'num_hitcircles': beatmap_db_content['num_hitcircles'],
        'num_sliders': beatmap_db_content['num_sliders'],
        'num_spinners': beatmap_db_content['num_spinners'],
        'approach_rate': beatmap_db_content['approach_rate'],
        'overall_difficulty': beatmap_db_content['overall_difficulty'],
        'circle_size': beatmap_db_content['circle_size'],
        'hp_drain': beatmap_db_content['hp_drain'],
        'last_played': beatmap_db_content['last_played'],
        'last_modified': beatmap_db_content['last_modified'],
        'last_modified2': beatmap_db_content['last_modified2'],
        'drain_time': beatmap_db_content['drain_time'],
        'total_time': beatmap_db_content['total_time'],
        'local_offset': beatmap_db_content['local_offset'],
        'import_source_hash': import_source_hash,
    }


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}
    
def fn(self: Task, session: Session, force_refresh: bool = False):
    """
        load parsed_osu_db_file.json

    """

    self.log_info('start_task')

    self.vars = {
        'to_import_items': None,
        'did_import_items': None,
        'num_items_to_import': None,
        'num_items_did_import': None,
        'failed_imports': None,
        'force_refresh': None,
    }

    osu_db_file_hash = utils.get_state__osu_db_file_hash(session)
    beatmap_data = utils.load_json__osu_db_file(osu_db_file_hash)['beatmap_data']

    beatmap_rows = []
    for beatmap in beatmap_data:
        row = get_table_row__beatmaps(beatmap, import_source_hash=osu_db_file_hash)
        if row['ranked_status'] == 1: continue
        beatmap_rows.append(row)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Beatmap)
        .where(Beatmap.import_source_hash == osu_db_file_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(beatmap_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=beatmap_rows,
            target_table=Beatmap,
            table_unique_key='beatmap_id',
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_beatmaps(force_refresh: bool = False, **kwargs):
    return Task(
        'task__populate_beatmaps',
        fn,
        log_messages,
        **kwargs,
        force_refresh=force_refresh,
    )
