from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.collections import Pack

import src.ingestion.tasks.zzz_common as task_common

from src.common.db import get_osu_api_data_cache_engine


def get_pack_mapping(pack_name: str, import_source_hash: str) -> dict:
    return {
        'name': pack_name,
        'import_type': 'API_DATA',
        'import_source_hash': import_source_hash,
    }


def get_already_populated_pack_names(session: Session) -> set:
    stmt_select_pack_names = select(Pack.name)
    return set(session.scalars(stmt_select_pack_names).all())


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

    already_populated_pack_names = get_already_populated_pack_names(session)

    print(f'{len(already_populated_pack_names)=}')

    pack_rows = []
    for pack in pack_data:
        pack_name = pack['tag']
        if pack_name in already_populated_pack_names: continue
        row = get_pack_mapping(
            pack_name=pack_name, 
            import_source_hash=pack_data_hash,
        )
        pack_rows.append(row)

    print(f'{len(pack_rows)=}')

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Pack)
        .where(Pack.import_source_hash == pack_data_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(pack_data_hash)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=pack_rows,
            target_table=Pack,
            table_unique_keys=['name'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_packs_api(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_packs_api',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
