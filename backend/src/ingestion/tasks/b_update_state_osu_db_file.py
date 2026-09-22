from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert

from orchestrator import Task, TaskStatus

import src.common.utils as utils

from src.common.models.misc import State


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}


def db_file_hash_in_state(self, db_file_hash: str, session: Session) -> bool:
    state_db_file_hash = utils.get_state__osu_db_file_hash(session)
    if db_file_hash != state_db_file_hash:
        return False
    return True


def fn(self: Task, session: Session, force_refresh: bool = False):
    """
    """

    self.log_info('start_task')

    self.vars = {
        'to_update_state': False,
        'did_update_state': False,
    }

    ## todo: should this db_file_hash be returned by the previous task (a_import)?
    db_file_hash = utils.md5_hash(utils.OSU_DB_FILE_PATH)

    if force_refresh:
        self.vars['force_refresh'] = True
    else:
        self.vars['to_update_state'] = not db_file_hash_in_state(self, db_file_hash, session)

    if self.vars['to_update_state'] or force_refresh:
        insert_stmt = insert(State).values(id=1, osu_db_file_hash=db_file_hash)
        do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=['id'], set_={'osu_db_file_hash': db_file_hash})
        session.execute(do_update_stmt)
        session.commit()
        self.vars['did_update_state'] = db_file_hash_in_state(self, db_file_hash, session)

    if not self.vars['to_update_state']:
        self.status = TaskStatus.SKIPPED
    else:
        self.status = TaskStatus.SUCCESS

    self.log_info('end_task')


def init_task__update_state_osu_db_file(force_refresh: bool = False, **kwargs):
    return Task(
        'task__update_state_osu_db_file',
        fn,
        log_messages,
        **kwargs,
        force_refresh=force_refresh,
    )
