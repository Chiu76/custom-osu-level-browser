import datetime

from sqlalchemy import Insert
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session, MappedClassProtocol

from orchestrator import Task


# https://gist.github.com/CarstenSchelp/b6fb490e8cc65e3ec7d62b950d1f3ad8
def ticks_to_posix(dotnet_ticks):
    if dotnet_ticks == 0: return 0
    _epoch = datetime.date(1970, 1 , 1)
    _dotnet_minvalue = datetime.date(1, 1, 1)
    _offset = (_epoch - _dotnet_minvalue).total_seconds()
    _ten_million = 10_000_000
    seconds = dotnet_ticks / _ten_million;
    posix =  seconds - _offset
    return round(posix)


def batch(items: list, size: int):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def get_on_conflict_set_(stmt: Insert) -> dict:
    return {
        column.key: stmt.excluded[column.key]
        for column in stmt.table.c
        if column.key not in ['id']
    }


def execute_upsert(row_contents: list[dict], target_table: MappedClassProtocol, table_unique_keys: list[str], session: Session):
    stmt = insert(target_table).values(row_contents)
    stmt = stmt.on_conflict_do_update(
        index_elements=table_unique_keys,
        set_=get_on_conflict_set_(stmt),
    )
    session.execute(stmt)
    session.commit()


def upsert_items(self: Task, row_contents: list[dict], target_table: MappedClassProtocol, table_unique_keys: list[str], session: Session):
    """
    
    """

    BATCH_SIZE = 1000

    self.vars['num_items_to_import'] = len(row_contents)
    self.vars['num_items_did_import'] = 0
    self.vars['failed_imports'] = []
    self.vars['did_import_items'] = True

    for row_content_batch in batch(row_contents, BATCH_SIZE):
        try:
            execute_upsert(row_content_batch, target_table, table_unique_keys, session)
            self.vars['num_items_did_import'] += len(row_content_batch)
        except:
            session.rollback()
            try:
                for row_content in row_content_batch:
                    execute_upsert(row_content, target_table, table_unique_keys, session)
                    self.vars['num_items_did_import'] += len(row_content)
            except Exception as e:
                session.rollback()
                self.vars['failed_imports'].append({
                    # table_unique_key: row_content[table_unique_key],
                    'exception': str(e),
                    'content': row_content,
                })
                if len(self.vars['failed_imports']) > int(self.vars['num_items_to_import'] * 0.02):
                    self.vars['did_import_items'] = False
                    break
