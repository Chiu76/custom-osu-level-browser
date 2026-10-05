from typing import Literal

import json
from pathlib import Path
import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.models.state import State


MODULE_DIR = Path(__file__).resolve().parent
SRC_DIR = MODULE_DIR.parent
PROJECT_DIR = SRC_DIR.parent

## todo: this can create a directory when called for a file: OSU_DB_FILE_PATH = _get_dir(DB_FILES_DIR / osu_db_file_name)
def _get_dir(dir: Path) -> Path:
    if not dir.exists(): dir.mkdir(parents=True)
    return dir

def _get_file_path(dir: Path, file_name: str, extension: str) -> Path:
    return _get_dir(dir / f'{file_name}.{extension}')

DATA_DIR = _get_dir(PROJECT_DIR / 'data')

DB_FILES_DIR = _get_dir(DATA_DIR / 'db_files')
IMPORTED_DB_FILES_DIR = _get_dir(DB_FILES_DIR / 'imported')
PARSED_DB_FILES_DIR = _get_dir(DB_FILES_DIR / 'parsed')

osu_db_file_name = 'osu!'
OSU_DB_FILE_PATH = _get_file_path(DB_FILES_DIR, osu_db_file_name, 'db')

collection_db_file_name = 'collection'
COLLECTION_DB_FILE_PATH = _get_file_path(DB_FILES_DIR, collection_db_file_name, 'db')

scores_db_file_name = 'scores'
SCORES_DB_FILE_PATH = _get_file_path(DB_FILES_DIR, scores_db_file_name, 'db')


def get_state__db_file_hash(
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    session: Session,
) -> str:
    state_column_dict = {
        'osu!': State.osu_db_file_hash,
        'collection': State.collection_db_file_hash,
        'scores': State.scores_db_file_hash,
    }
    stmt = select(state_column_dict[db_file_type])    
    hash = session.scalars(stmt).one_or_none()
    return hash


def load_json__db_file(
    db_file_type: Literal['osu!', 'collection', 'scores'], 
    db_file_hash: str,
) -> dict:
    parsed_osu_db_file_path = PARSED_DB_FILES_DIR / f'{db_file_type}_{db_file_hash}.json'
    return json.loads(parsed_osu_db_file_path.read_text())


def md5_hash(file_path: Path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()