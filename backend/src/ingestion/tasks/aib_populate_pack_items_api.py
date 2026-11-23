import json

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap
from src.common.models.collections import Pack, PackItem

import src.ingestion.tasks.zzz_common as task_common

from src.common.db import get_osu_api_data_cache_engine


def get_pack_item_mapping(pack_id: int, beatmap_db_id: int, import_source_hash: str) -> dict:
    return {
        'pack_id': pack_id,
        'beatmap_db_id': beatmap_db_id,
        'import_type': 'API_DATA',
        'import_source_hash': import_source_hash,
    }


def get_osu_api_data_cache__packs():
    engine = get_osu_api_data_cache_engine()
    with engine.connect() as conn:
        ## todo: remember this is hardcoded for osu!std
        results = conn.execute(
            text('''
            SELECT tag, beatmapset_ids
            FROM beatmap_packs
            WHERE ruleset_id is null or ruleset_id == 0;
            ''')
        ).mappings().all()
    return [dict(row) for row in results]


def get_dict__name_to_pack_id(session: Session):
    pack_name_and_id = session.execute(select(Pack.name, Pack.id)).all()
    return { name: pack_id for name, pack_id in pack_name_and_id }


def get_dict__beatmapset_id_to_beatmap_db_ids(session: Session):
    beatmapset_id_to_beatmap_db_ids = {}

    beatmap_db_id_and_set_id = session.execute(select(Beatmap.id, Beatmap.beatmapset_id)).all()

    for db_id, set_id in beatmap_db_id_and_set_id:
        if beatmapset_id_to_beatmap_db_ids.get(set_id) == None:
            beatmapset_id_to_beatmap_db_ids[set_id] = [db_id]
        else:
            beatmapset_id_to_beatmap_db_ids[set_id].append(db_id)
    
    return beatmapset_id_to_beatmap_db_ids


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

    pack_data = get_osu_api_data_cache__packs()
    pack_data_hash = utils.md5_hash_dict(pack_data)

    name_to_pack_id = get_dict__name_to_pack_id(session)
    beatmapset_id_to_beatmap_db_ids = get_dict__beatmapset_id_to_beatmap_db_ids(session)
    
    pack_rows = []
    for pack in pack_data:
        for beatmapset_id in json.loads(pack['beatmapset_ids']):
            pack_id = name_to_pack_id[pack['tag']]
            beatmap_db_ids = beatmapset_id_to_beatmap_db_ids.get(beatmapset_id)
            if not beatmap_db_ids: continue
            for beatmap_db_id in beatmap_db_ids:
                row = get_pack_item_mapping(pack_id, beatmap_db_id, import_source_hash=pack_data_hash)
                pack_rows.append(row)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(PackItem)
        .where(PackItem.import_source_hash == pack_data_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(pack_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=pack_rows,
            target_table=PackItem,
            table_unique_keys=['pack_id', 'beatmap_db_id'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_pack_items_api(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_pack_items_api',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
