from sqlalchemy import select, func
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap
from src.common.models.scores import Score

import src.ingestion.tasks.zzz_common as task_common


def compute_grade(score: dict):
    num_300s = score['num_300s']
    num_100s = score['num_100s']
    num_50s = score['num_50s']
    num_misses = score['num_misses']

    total_hits = num_300s + num_100s + num_50s + num_misses

    all_300s = num_300s == total_hits
    over_90_percent_300s = num_300s * 100 > total_hits * 90
    over_80_percent_300s = num_300s * 100 > total_hits * 80
    over_70_percent_300s = num_300s * 100 > total_hits * 70
    over_60_percent_300s = num_300s * 100 > total_hits * 60
    at_most_1_percent_50s = num_50s * 100 <= total_hits

    if all_300s:
        return 'SS'
    elif over_90_percent_300s and at_most_1_percent_50s and num_misses == 0:
        return 'S'
    elif (over_80_percent_300s and num_misses == 0) or over_90_percent_300s:
        return 'A'
    elif (over_70_percent_300s and num_misses == 0) or over_80_percent_300s:
        return 'B'
    elif over_60_percent_300s:
        return 'C'
    else:
        return 'D'


def get_score_mapping(beatmap_db_id: int, score: dict, import_source_hash: str) -> dict:
    return {
        'beatmap_db_id': beatmap_db_id,
        'mode': score['mode'],
        'version': score['version'],
        'player_name': score['player_name'],
        'beatmap_md5_hash': score['md5'],
        'replay_md5_hash': score['replay_md5'],
        'num_300s': score['num_300s'],
        'num_100s': score['num_100s'],
        'num_50s': score['num_50s'],
        'num_gekis': score['num_gekis'],
        'num_katus': score['num_katus'],
        'num_misses': score['num_misses'],
        'grade': compute_grade(score),
        'replay_score': score['replay_score'],
        'max_combo': score['max_combo'],
        'perfect_combo': score['perfect_combo'],
        'mods': score['mods'],
        'timestamp': score['timestamp'],
        'online_score_id': score['online_score_id'],
        'import_source_hash': import_source_hash,
    }


def get_dict__hash_to_beatmap_db_id(score_data_per_beatmap: dict, session: Session):
    hashes_to_import = set()
    for beatmap_md5_hash in score_data_per_beatmap:
        hashes_to_import.add(beatmap_md5_hash)

    stmt_select_beatmap_hash_and_id = (
        select(Beatmap.md5_hash, Beatmap.id)
        .where(Beatmap.md5_hash.in_(hashes_to_import))
    )
    beatmap_hash_and_id = session.execute(stmt_select_beatmap_hash_and_id).all()
    
    return { hash: beatmap_db_id for hash, beatmap_db_id in beatmap_hash_and_id }


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

    db_file_hash = utils.get_state__db_file_hash('scores', session)
    score_data_per_beatmap = utils.load_json__db_file('scores', db_file_hash)['beatmaps']

    ## todo: keep track of how many scores are not imported due to possible possible beatmap hash without a db id
    hash_to_beatmap_db_id = get_dict__hash_to_beatmap_db_id(score_data_per_beatmap, session)

    score_rows = []
    for beatmap_md5_hash in score_data_per_beatmap:
        beatmap_db_id = hash_to_beatmap_db_id.get(beatmap_md5_hash)
        if not beatmap_db_id: continue
        for score in score_data_per_beatmap[beatmap_md5_hash]:
            mapping = get_score_mapping(beatmap_db_id, score, db_file_hash)
            score_rows.append(mapping)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Score)
        .where(Score.import_source_hash == db_file_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(score_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=score_rows,
            target_table=Score,
            table_unique_keys=['beatmap_md5_hash', 'replay_md5_hash'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_scores(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_scores',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
