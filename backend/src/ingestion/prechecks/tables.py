from sqlalchemy import Engine, inspect, select
from sqlalchemy.orm import Session

from src.common.models.misc import State

from orchestrator import Task, TaskStatus


def init_precheck__table_exists(engine: Engine, table: str):
    def fn(self: Task):
        self.vars = {'table': table, 'table_exists': False}
        table_names = inspect(engine).get_table_names()
        if table not in table_names:
            self.status = TaskStatus.FAILED
        self.vars['table_exists'] = True
        self.status = TaskStatus.SUCCESS
    return Task('precheck__table_exists', fn)


def init_precheck__state_table_populated():
    def fn(self: Task):
        self.vars = {'table': 'state', 'table_populated': False}
        state = self.session.scalars(select(State.osu_db_file_hash)).one_or_none()
        if state is None:
            self.status = TaskStatus.FAILED
        self.vars['table_populated'] = True
        self.status = TaskStatus.SUCCESS
    return Task('precheck__state_table_populated', fn)
