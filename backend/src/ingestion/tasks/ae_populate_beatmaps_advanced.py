import json

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap

import src.ingestion.tasks.zzz_common as task_common

from src.common.db import get_osu_api_data_cache_engine


def compute_bpm(timing_points: list) -> float:
    if len(timing_points) == 1:
        return round(60_000 / timing_points[0]['beat_length'])
    
    bpm_counts = {}
    for timing_point in timing_points:
        bpm = round(60_000 / timing_point['beat_length'])
        if bpm not in bpm_counts:
            bpm_counts[bpm] = 1
        else:
            bpm_counts[bpm] += 1
    bpm_counts_as_sorted_list = list(sorted(bpm_counts.items(), key=lambda item: item[1], reverse=True))
    
    return bpm_counts_as_sorted_list[0][0]


def get_beatmap_mapping(beatmap_db_content: dict, import_source_hash: str) -> dict:
    return {
        'beatmap_set_id': beatmap_db_content['beatmapset_id'],
        'beatmap_id': beatmap_db_content['id'],
        'md5_hash': beatmap_db_content['checksum'],
        'mode': beatmap_db_content['mode'],
        'difficulty_name': beatmap_db_content['version'],
        'bpm': beatmap_db_content['bpm'],
        'audio_file': '',
        'map_file': '',
        'ranked_status': beatmap_db_content['status'],
        'num_hitcircles': beatmap_db_content['count_circles'],
        'num_sliders': beatmap_db_content['count_sliders'],
        'num_spinners': beatmap_db_content['count_spinners'],
        'approach_rate': beatmap_db_content['ar'],
        'overall_difficulty': beatmap_db_content['accuracy'],
        'circle_size': beatmap_db_content['cs'],
        'hp_drain': beatmap_db_content['drain'],
        'last_played': task_common.ticks_to_posix(0),
        'last_modified': task_common.ticks_to_posix(0),
        'drain_time': beatmap_db_content['hit_length'],
        'total_time': beatmap_db_content['total_length'],
        'local_offset': 0,
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

    db_file_hash = utils.get_state__db_file_hash('osu!', session)
    beatmap_set_data = get_osu_api_data_cache__beatmapsets()

    beatmap_rows = []
    for beatmap_set in beatmap_set_data:
        beatmaps = json.loads(beatmap_set['content'])['beatmaps']
        for beatmap in beatmaps:
            row = get_beatmap_mapping(beatmap, import_source_hash=db_file_hash)
            beatmap_rows.append(row)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Beatmap)
        .where(Beatmap.import_source_hash == db_file_hash)
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


def init_task__populate_beatmaps_advanced(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_beatmaps_advanced',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
