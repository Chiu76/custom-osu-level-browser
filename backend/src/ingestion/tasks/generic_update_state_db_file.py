from typing import Literal
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert

from orchestrator import Task, TaskStatus

import src.common.utils as utils

from src.common.models.state import State


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}


def get_upsert_state_stmt(db_file_hash: str, db_file_type: Literal['osu!', 'collection', 'scores']):
    insert_stmt = insert(State)
    if db_file_type == 'osu!':
        insert_stmt = insert_stmt.values(id=1, osu_db_file_hash=db_file_hash)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['id'], 
            set_={'osu_db_file_hash': db_file_hash},
        )
    elif db_file_type == 'collection':
        insert_stmt = insert_stmt.values(id=1, collection_db_file_hash=db_file_hash)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['id'], 
            set_={'collection_db_file_hash': db_file_hash},
        )
    elif db_file_type == 'scores':
        insert_stmt = insert_stmt.values(id=1, scores_db_file_hash=db_file_hash)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['id'], 
            set_={'scores_db_file_hash': db_file_hash},
        )
    return upsert_stmt


def fn(self: Task, 
    session: Session, 
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    db_file_path: Path, 
    force_refresh: bool = False
):
    """
    """

    self.log_info('start_task')

    self.vars = {
        'to_update_state': False,
        'did_update_state': False,
    }

    ## todo: should this db_file_hash be returned by the previous task (a_import)?
    db_file_hash = utils.md5_hash(db_file_path)

    if force_refresh:
        self.vars['force_refresh'] = True
    else:
        self.vars['to_update_state'] = not db_file_hash == utils.get_state__db_file_hash(db_file_type, session)

    if self.vars['to_update_state'] or force_refresh:
        upsert_state_stmt = get_upsert_state_stmt(db_file_hash, db_file_type)
        session.execute(upsert_state_stmt)
        session.commit()
        self.vars['did_update_state'] = db_file_hash == utils.get_state__db_file_hash(db_file_type, session)

    if not self.vars['to_update_state']:
        self.status = TaskStatus.SKIPPED
    else:
        self.status = TaskStatus.SUCCESS

    self.log_info('end_task')


def init_task__generic_update_state_db_file(
    session: Session,
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    db_file_path: Path, 
    force_refresh: bool = False,
):
    return Task(
        f'task__generic_update_state_db_file_{db_file_type}',
        fn,
        log_messages,
        session,
        db_file_type,
        db_file_path,
        force_refresh=force_refresh,
    )
