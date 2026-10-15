from sqlalchemy import select, func
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap, BeatmapStarRating

import src.ingestion.tasks.zzz_common as task_common


def get_beatmap_star_rating_mapping(
    beatmap_db_id: int, 
    mode: int, 
    mods: int, 
    star_rating: float, 
    import_source_hash: str
) -> dict:
    return {
        'beatmap_db_id': beatmap_db_id,
        'mode': mode,
        'mods': mods,
        'star_rating': round(star_rating, 2),
        'import_source_hash': import_source_hash,
    }


def get_dict__beatmap_id_to_db_id(import_source_hash: str, session: Session) -> dict:
    stmt_select_beatmap_hash_and_id = (
        select(Beatmap.beatmap_id, Beatmap.id)
        .where(Beatmap.import_source_hash == import_source_hash)
    )
    beatmap_id_and_db_id = session.execute(stmt_select_beatmap_hash_and_id).all()
    
    return { beatmap_id: beatmap_db_id for beatmap_id, beatmap_db_id in beatmap_id_and_db_id }


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
    beatmap_data = utils.load_json__db_file("osu!", db_file_hash)['beatmap_data']

    beatmap_id_to_db_id = get_dict__beatmap_id_to_db_id(db_file_hash, session)

    beatmap_star_rating_rows = []
    for beatmap in beatmap_data:
        beatmap_db_id = beatmap_id_to_db_id.get(beatmap['beatmap_id'])
        if not beatmap_db_id: continue
        for mode in beatmap['star_ratings']:
            ## todo: std only for now
            if int(mode) != 0: continue
            for mods, star_rating in beatmap['star_ratings'][mode]:
                row = get_beatmap_star_rating_mapping(
                    beatmap_db_id,
                    mode,
                    mods,
                    star_rating,
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


def init_task__populate_beatmap_star_ratings(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_beatmap_star_ratings',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
