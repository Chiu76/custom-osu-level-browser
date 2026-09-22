import json
from sqlalchemy.orm import Session

from osu_db_tools.osu_to_python import osu_to_python as parse_osu_db

from orchestrator import Task, TaskStatus

import src.common.utils as utils


old_log_messages = {
    'start_task': 'TASK_START: starting task',
    'force_refresh': 'TASK_UPDATE: force_refresh, forcefully (re)parsing ingested osu!.db file (ingested_osu_db_file_hash={})',
    'to_parse_db_file': 'TASK_UPDATE: to_parse_db_file: about to parse ingested osu!.db file (ingested_osu_db_file_hash={})',
    'not_parsing_db_file': 'TASK_UPDATE: not_parsing_db_file: found already existing parsed_osu_db_file_name={}, therefore not parsing ingested osu!.db file (ingested_osu_db_file_hash={})',
    'parsed_db_file': 'TASK_UPDATE: parsed_db_file: successfully parsed ingested osu!.db file (ingested_osu_db_file_hash={})',
    'end_task': 'TASK_END: ending task',
}


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}
    
def fn(self: Task, session: Session, force_refresh: bool = False):
    """
    """

    self.log_info('start_task')

    self.vars = {
        'to_parse_file': False,
        'did_parse_file': False,
    }

    osu_db_file_hash = utils.get_state__osu_db_file_hash(session)

    imported_file_path = utils.IMPORTED_DB_FILES_DIR / f'osu!{osu_db_file_hash}.db'
    parsed_file_path = utils.PARSED_DB_FILES_DIR / f'osu!{osu_db_file_hash}.json'

    if force_refresh:
        self.vars['force_refresh'] = True
    else:
        self.vars['to_parse_file'] = not parsed_file_path.exists()

    if self.vars['to_parse_file'] or force_refresh:
        content = parse_osu_db(imported_file_path)
        parsed_file_path.write_text(json.dumps(content))
        # parsed_file_path.write_text(json.dumps(content, indent=4))
        self.vars['did_parse_file'] = parsed_file_path.exists()
    
    if not self.vars['to_parse_file']:
        self.status = TaskStatus.SKIPPED
    else:
        self.status = TaskStatus.SUCCESS

    self.log_info('end_task')


def init_task__parse_imported_osu_db_file(force_refresh: bool = False, **kwargs):
    return Task(
        'task__parse_imported_osu_db_file',
        fn,
        log_messages,
        **kwargs,
        force_refresh=force_refresh,
    )
