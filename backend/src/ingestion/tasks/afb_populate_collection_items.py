from sqlalchemy import select, func
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.beatmaps import Beatmap
from src.common.models.collections import Collection, CollectionItem

import src.ingestion.tasks.zzz_common as task_common


def get_collection_item_mapping(collection_id: int, beatmap_db_id: int, md5_hash: str, import_source_hash: str) -> dict:
    return {
        'collection_id': collection_id,
        'beatmap_db_id': beatmap_db_id,
        'md5_hash': md5_hash,
        'import_source_hash': import_source_hash,
    }


def get_dict__name_to_collection_id(collection_data: dict, session: Session):
    collection_names_to_import = set()
    for col in collection_data:
        collection_names_to_import.add(col['name'])

    stmt_select_collection_name_and_id = (
        select(Collection.name, Collection.id)
        .where(Collection.name.in_(collection_names_to_import))
    )
    collection_name_and_id = session.execute(stmt_select_collection_name_and_id).all()
    
    return { name: collection_id for name, collection_id in collection_name_and_id }


def get_dict__hash_to_beatmap_db_id(collection_data: dict, session: Session):
    hashes_to_import = set()
    for col in collection_data:
        for hash in col['hashes']:
            hashes_to_import.add(hash)

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

    db_file_hash = utils.get_state__db_file_hash('collection', session)
    collection_data = utils.load_json__db_file("collection", db_file_hash)['collections']

    ## todo: keep track of how many collection items are not imported due to below: possible collection name without an id, possible beatmap hash without a db id
    name_to_collection_id = get_dict__name_to_collection_id(collection_data, session)
    hash_to_beatmap_db_id = get_dict__hash_to_beatmap_db_id(collection_data, session)

    collection_item_rows = []
    for col in collection_data:
        collection_id = name_to_collection_id[col['name']]
        for hash in col['hashes']:
            beatmap_db_id = hash_to_beatmap_db_id.get(hash)
            if not beatmap_db_id: continue
            mapping = get_collection_item_mapping(collection_id, beatmap_db_id, hash, db_file_hash)
            collection_item_rows.append(mapping)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(CollectionItem)
        .where(CollectionItem.import_source_hash == db_file_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(collection_item_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=collection_item_rows,
            target_table=CollectionItem,
            table_unique_keys=['collection_id', 'beatmap_db_id'],
            session=session,
        )

    if not self.vars['to_import_items'] and not self.vars['force_refresh']:
        self.status = TaskStatus.SKIPPED
    elif self.vars['did_import_items']:
        self.status = TaskStatus.SUCCESS
    else:
        self.status = TaskStatus.FAILED

    self.log_info('end_task')


def init_task__populate_collection_items(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_collection_items',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
