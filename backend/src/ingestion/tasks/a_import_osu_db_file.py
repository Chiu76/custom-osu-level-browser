from shutil import copyfile

from orchestrator import Task, TaskStatus

import src.common.utils as utils


old_log_messages = {
    'start_task': 'TASK_START: starting task',
    'force_refresh': 'TASK_UPDATE: force_refresh: forcefully (re)ingesting osu!.db file with fresh_osu_db_file_hash={})',
    'to_update_state': 'TASK_UPDATE: to_update_state: about to update state with the latest osu!.db file hash (fresh_osu_db_file_hash={})',
    'not_to_update_state': 'TASK_UPDATE: not_to_update_state: not updating state, latest osu!.db\'s file hash already in current state (fresh_osu_db_file_hash={})',
    'updated_state': 'TASK_UPDATE: updated_state: successfully updated state with latest osu!.db file hash (fresh_osu_db_file_hash={})',
    'to_copy_db_file': 'TASK_UPDATE: to_copy_db_file: about to copy ingested_osu_db_file_name={} to `ingested_db_files` directory',
    'not_to_copy_db_file': 'TASK_UPDATE: not_to_copy_db_file: not copying ingested_osu_db_file_name={} to `ingested_db_files` directory, it already exists',
    'copied_db_file': 'TASK_UPDATE: copied_db_file: successfully copied the ingested_osu_db_file_name={} to `ingested_db_files` directory',
    'end_task': 'TASK_END: ending task',
}


log_messages = {
    'start_task': 'TASK_START: start_task',
    'end_task': 'TASK_END: end_task',
}
    
def fn(self: Task, force_refresh: bool = False):
    """
    """

    self.log_info('start_task')

    self.vars = {
        'to_copy_file': None,
        'did_copy_file': None,
        'force_refresh': None,
    }

    db_hash = utils.md5_hash(utils.OSU_DB_FILE_PATH)
    imported_file_path = utils.IMPORTED_DB_FILES_DIR / f'osu!{db_hash}.db'

    if force_refresh:
        self.vars['force_refresh'] = True
    else:
        self.vars['to_copy_file'] = not imported_file_path.exists()

    if self.vars['to_copy_file'] or force_refresh:
        copyfile(utils.OSU_DB_FILE_PATH, imported_file_path)
        self.vars['did_copy_file'] = imported_file_path.exists()

    if not self.vars['to_copy_file']:
        self.status = TaskStatus.SKIPPED
    else:
        self.status = TaskStatus.SUCCESS

    self.log_info('end_task')


def init_task__import_osu_db_file(force_refresh: bool = False):
    return Task(
        'task__import_osu_db_file',
        fn,
        log_messages,
        force_refresh=force_refresh,
    )
