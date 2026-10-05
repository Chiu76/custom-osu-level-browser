from typing import Literal
from pathlib import Path

import json
from sqlalchemy.orm import Session

from osu_db_tools.osu_to_python import osu_to_python as parse_osu_db
from osu_db_tools.read_collection import collection_to_dict as parse_collection_db
from osu_db_tools.parse_scores import unpack_scores as parse_scores_db

from orchestrator import Task, TaskStatus

import src.common.utils as utils


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}

def parse_db_file(
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    imported_file_path: Path,
):
    if db_file_type == 'osu!':
        return parse_osu_db(imported_file_path)
    elif db_file_type == 'collection':
        return parse_collection_db(imported_file_path)
    elif db_file_type == 'scores':
        return parse_scores_db(imported_file_path)
    
def fn(
    self: Task,     
    session: Session, 
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    force_refresh: bool = False,
):
    self.log_info('start_task')

    self.vars = {
        'to_parse_file': False,
        'did_parse_file': False,
    }

    db_file_hash = utils.get_state__db_file_hash(db_file_type, session)

    imported_file_path = utils.IMPORTED_DB_FILES_DIR / f'{db_file_type}_{db_file_hash}.db'
    parsed_file_path = utils.PARSED_DB_FILES_DIR / f'{db_file_type}_{db_file_hash}.json'

    if force_refresh:
        self.vars['force_refresh'] = True
    else:
        self.vars['to_parse_file'] = not parsed_file_path.exists()

    if self.vars['to_parse_file'] or force_refresh:
        parsed_file_content = parse_db_file(db_file_type, imported_file_path)
        # parsed_file_path.write_text(json.dumps(parsed_file_content))
        parsed_file_path.write_text(json.dumps(parsed_file_content, indent=4))
        self.vars['did_parse_file'] = parsed_file_path.exists()
    
    if not self.vars['to_parse_file']:
        self.status = TaskStatus.SKIPPED
    else:
        self.status = TaskStatus.SUCCESS

    self.log_info('end_task')


def init_task__generic_parse_imported_db_file(
    session: Session, 
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    force_refresh: bool = False,
):
    return Task(
        f'task__generic_parse_imported_db_file_{db_file_type}',
        fn,
        log_messages,
        session,
        db_file_type,
        force_refresh=force_refresh,
    )
