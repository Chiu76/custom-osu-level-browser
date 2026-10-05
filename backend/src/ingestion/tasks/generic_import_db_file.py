from typing import Literal
from pathlib import Path
from shutil import copyfile

from orchestrator import Task, TaskStatus

import src.common.utils as utils


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}
    
def fn(
    self: Task, 
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    db_file_path: Path, 
    force_refresh: bool = False,
):
    self.log_info('start_task')

    self.vars = {
        'to_copy_file': None,
        'did_copy_file': None,
        'force_refresh': None,
    }

    db_file_hash = utils.md5_hash(db_file_path)
    imported_file_path = utils.IMPORTED_DB_FILES_DIR / f'{db_file_type}_{db_file_hash}.db'

    if force_refresh:
        self.vars['force_refresh'] = True
    else:
        self.vars['to_copy_file'] = not imported_file_path.exists()

    if self.vars['to_copy_file'] or force_refresh:
        copyfile(db_file_path, imported_file_path)
        self.vars['did_copy_file'] = imported_file_path.exists()

    if not self.vars['to_copy_file']:
        self.status = TaskStatus.SKIPPED
    else:
        self.status = TaskStatus.SUCCESS

    self.log_info('end_task')


def init_task__generic_import_db_file(
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    db_file_path: Path, 
    force_refresh: bool = False,
):
    return Task(
        f'task__generic_import_db_file_{db_file_type}',
        fn,
        log_messages,
        db_file_type,
        db_file_path,
        force_refresh=force_refresh,
    )
