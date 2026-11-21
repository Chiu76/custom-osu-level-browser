from sqlalchemy import select, func
from sqlalchemy.orm import Session

from orchestrator import Task, TaskStatus

import src.common.utils as utils
from src.common.models.collections import Collection

import src.ingestion.tasks.zzz_common as task_common


def get_collection_mapping(collection_db_content: dict, import_source_hash: str) -> dict:
    return {
        'name': collection_db_content['name'],
        'import_source_hash': import_source_hash,
    }


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

    collection_rows = []
    for collection in collection_data:
        mapping = get_collection_mapping(collection, import_source_hash=db_file_hash)
        collection_rows.append(mapping)

    already_imported_count = session.scalar(
        select(func.count())
        .select_from(Collection)
        .where(Collection.import_source_hash == db_file_hash)
    )

    self.vars['to_import_items'] = already_imported_count != len(collection_rows)
    self.vars['force_refresh'] = force_refresh

    if self.vars['to_import_items'] or self.vars['force_refresh']:
        task_common.upsert_items(
            self=self,
            row_contents=collection_rows,
            target_table=Collection,
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


def init_task__populate_collections(session: Session, force_refresh: bool = False):
    return Task(
        'task__populate_collections',
        fn,
        log_messages,
        session,
        force_refresh=force_refresh,
    )
