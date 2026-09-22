import json
from pathlib import Path
import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.models.misc import State


MODULE_DIR = Path(__file__).resolve().parent
SRC_DIR = MODULE_DIR.parent
PROJECT_DIR = SRC_DIR.parent

## todo: this can create a directory when called for a file: OSU_DB_FILE_PATH = _get_dir(DB_FILES_DIR / osu_db_file_name)
def _get_dir(dir: Path):
    if not dir.exists(): dir.mkdir(parents=True)
    return dir

DATA_DIR = _get_dir(PROJECT_DIR / 'data')

DB_FILES_DIR = _get_dir(DATA_DIR / 'db_files')
IMPORTED_DB_FILES_DIR = _get_dir(DB_FILES_DIR / 'imported')
PARSED_DB_FILES_DIR = _get_dir(DB_FILES_DIR / 'parsed')

osu_db_file_name = 'osu!.db'
OSU_DB_FILE_PATH = _get_dir(DB_FILES_DIR / osu_db_file_name)


def get_state__osu_db_file_hash(session: Session) -> str:
    stmt = select(State.osu_db_file_hash)
    hash = session.scalars(stmt).one_or_none()
    return hash


def load_json__osu_db_file(osu_db_file_hash: str) -> dict:
    parsed_osu_db_file_path = PARSED_DB_FILES_DIR / f'osu!{osu_db_file_hash}.json'
    return json.loads(parsed_osu_db_file_path.read_text())


def md5_hash(file_path: Path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()