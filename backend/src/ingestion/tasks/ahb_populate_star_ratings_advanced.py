from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap, BeatmapStarRating

import src.ingestion.tasks.zzz_common as task_common

from src.common.db import get_osu_api_data_cache_engine


def get_beatmap_star_rating_mapping(
    beatmap_db_id: int, 
    mode: int, 
    mods: int, 
    star_rating: float, 
    star_rating_aim: float, 
    star_rating_speed: float, 
    star_rating_reading: float, 
    import_source_hash: str
) -> dict:
    return {
        'beatmap_db_id': beatmap_db_id,
        'mode': mode,
        'mods': mods,
        'star_rating': star_rating,
        'star_rating_aim': star_rating_aim,
        'star_rating_speed': star_rating_speed,
        'star_rating_reading': star_rating_reading,
        'import_source_hash': import_source_hash,
    }


def get_dict__beatmap_id_to_db_id(import_source_hash: str, session: Session) -> dict:
    stmt_select_beatmap_hash_and_id = (
        select(Beatmap.beatmap_id, Beatmap.id)
        .where(Beatmap.import_source_hash == import_source_hash)
    )
    beatmap_id_and_db_id = session.execute(stmt_select_beatmap_hash_and_id).all()
    
    return { beatmap_id: beatmap_db_id for beatmap_id, beatmap_db_id in beatmap_id_and_db_id }


def get_osu_api_data_cache__star_ratings():
    engine = get_osu_api_data_cache_engine()
    with engine.connect() as conn:
        results = conn.execute(
            text('''
                SELECT version, beatmap_id, mode, mods, star_rating, star_rating_aim, star_rating_speed, star_rating_reading
                FROM beatmap_star_ratings;
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
    beatmap_star_ratings_data = get_osu_api_data_cache__star_ratings()

    beatmap_id_to_db_id = get_dict__beatmap_id_to_db_id(db_file_hash, session)

    beatmap_star_rating_rows = []
    for beatmap in beatmap_star_ratings_data:
        beatmap_db_id = beatmap_id_to_db_id.get(beatmap['beatmap_id'])
        if not beatmap_db_id: continue
        row = get_beatmap_star_rating_mapping(
            beatmap_db_id,
            beatmap['mode'],
            beatmap['mods'],
            beatmap['star_rating'],
            beatmap['star_rating_aim'],
            beatmap['star_rating_speed'],
            beatmap['star_rating_reading'],
            import_source_hash=db_file_hash
        )
        beatmap_star_rating_rows.append(row)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(BeatmapStarRating)
        .where(BeatmapStarRating.import_source_hash == db_file_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(beatmap_star_rating_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=beatmap_star_rating_rows,
            target_table=BeatmapStarRating,
            table_unique_keys=['beatmap_db_id', 'mode', 'mods'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_beatmap_star_ratings_advanced(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_beatmap_star_ratings_advanced',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
