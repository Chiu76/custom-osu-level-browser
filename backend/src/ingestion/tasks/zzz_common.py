from sqlalchemy import Insert
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session, MappedClassProtocol

from orchestrator import Task


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


def execute_upsert(row_contents: list[dict], target_table: MappedClassProtocol, table_unique_key: str, session: Session):
    stmt = insert(target_table).values(row_contents)
    stmt = stmt.on_conflict_do_update(
        index_elements=[table_unique_key],
        set_=get_on_conflict_set_(stmt),
    )
    session.execute(stmt)
    session.commit()


def upsert_items(self: Task, row_contents: list[dict], target_table: MappedClassProtocol, table_unique_key: str, session: Session):
    """
    
    """

    BATCH_SIZE = 1000

    self.vars['num_items_to_import'] = len(row_contents)
    self.vars['num_items_did_import'] = 0
    self.vars['failed_imports'] = []
    self.vars['did_import_items'] = True

    for row_content_batch in batch(row_contents, BATCH_SIZE):
        try:
            execute_upsert(row_content_batch, target_table, table_unique_key, session)
            self.vars['num_items_did_import'] += len(row_content_batch)
        except:
            session.rollback()
            try:
                for row_content in row_content_batch:
                    execute_upsert(row_content, target_table, table_unique_key, session)
                    self.vars['num_items_did_import'] += len(row_content)
            except Exception as e:
                session.rollback()
                self.vars['failed_imports'].append({
                    table_unique_key: row_content[table_unique_key],
                    'exception': str(e),
                    'content': row_content,
                })
                if len(self.vars['failed_imports']) > int(self.vars['num_items_to_import'] * 0.02):
                    self.vars['did_import_items'] = False
                    break
