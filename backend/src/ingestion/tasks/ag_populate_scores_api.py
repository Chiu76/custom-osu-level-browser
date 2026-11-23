import json

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap
from src.common.models.scores import Score

import src.ingestion.tasks.zzz_common as task_common

from src.api.score_query.yyy_mods import get_mods_value

from src.common.db import get_osu_api_data_cache_engine


def get_score_mapping(beatmap_db_id: int, score: dict, import_source_hash: str) -> dict:
    return {
        'beatmap_db_id': beatmap_db_id,
        'online_score_id': score['id'],
        'mode': score['mode'],
        'mods': get_mods_value(score['mods']),
        'num_300s': score['statistics']['count_300'],
        'num_100s': score['statistics']['count_100'],
        'num_50s': score['statistics']['count_50'],
        'num_gekis': score['statistics']['count_geki'],
        'num_katus': score['statistics']['count_katu'],
        'num_misses': score['statistics']['count_miss'],
        'grade': score['rank'],
        'accuracy': round(score['accuracy'] * 100, 2),
        'replay_score': score['score'],
        'max_combo': score['max_combo'],
        'perfect_combo': score['perfect'],
        'played_at': task_common.osu_api_timestamp_to_posix(score['created_at']),

        'player_id': score['user_id'],
        'passed': score['passed'],
        'pp': score['pp'],
        
        'import_type': 'STABLE_LOCAL_DATA',
        'import_source_hash': import_source_hash,
    }


def get_osu_api_data_cache__user_beatmap_scores(user_id: int):
    engine = get_osu_api_data_cache_engine()
    with engine.connect() as conn:
        results = conn.execute(
            text(f'''
            SELECT beatmap_id, content 
            FROM user_beatmap_scores
            WHERE user_id = {user_id}; 
            ''')
        ).mappings().all()
    return [dict(row) for row in results]


def get_dict__beatmap_id_to_beatmap_db_id(user_beatmap_scores_data: list[dict], session: Session):
    beatmap_ids_to_import = set()
    for user_beatmap_score in user_beatmap_scores_data:
        beatmap_ids_to_import.add(user_beatmap_score['beatmap_id'])

    stmt_select_beatmap_id_and_db_id = (
        select(Beatmap.beatmap_id, Beatmap.id)
        .where(Beatmap.beatmap_id.in_(beatmap_ids_to_import))
    )
    beatmap_id_and_db_id = session.execute(stmt_select_beatmap_id_and_db_id).all()
    
    return { id: db_id for id, db_id in beatmap_id_and_db_id }


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}
    
def fn(self: Task, user_id: int, session: Session, force_refresh: bool = False):
    self.log_info('start_task')

    self.vars = {
        'to_import_items': None,
        'did_import_items': None,
        'num_items_to_import': None,
        'num_items_did_import': None,
        'failed_imports': None,
        'force_refresh': None,
    }

    user_beatmap_scores_data = get_osu_api_data_cache__user_beatmap_scores(user_id)
    user_beatmap_scores_data_hash = utils.md5_hash_dict(user_beatmap_scores_data)

    ## todo: keep track of how many scores are not imported due to possible possible beatmap hash without a db id
    beatmap_id_to_beatmap_db_id = get_dict__beatmap_id_to_beatmap_db_id(user_beatmap_scores_data, session)
    
    score_rows = []
    for user_beatmap_scores in user_beatmap_scores_data:
        beatmap_db_id = beatmap_id_to_beatmap_db_id.get(user_beatmap_scores['beatmap_id'])
        if not beatmap_db_id: continue
        for score in json.loads(user_beatmap_scores['content']):
            mapping = get_score_mapping(beatmap_db_id, score, user_beatmap_scores_data_hash)
            score_rows.append(mapping)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Score)
        .where(Score.import_source_hash == user_beatmap_scores_data_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(score_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=score_rows,
            target_table=Score,
            table_unique_keys=['id'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_scores_api(user_id: int, session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_scores_api',
        fn,
        log_messages,
        user_id,
        session,
        force_refresh=force_refresh,
    )
