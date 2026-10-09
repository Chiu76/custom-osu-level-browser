from sqlalchemy.orm import Session

from src.common.db import engine, SessionMaker

from orchestrator import Job

import src.common.utils as utils

from ..prechecks.tables import init_precheck__table_exists
from ..prechecks.tables import init_precheck__state_table_populated

from ..tasks.generic_import_db_file import init_task__generic_import_db_file 
from ..tasks.generic_update_state_db_file import init_task__generic_update_state_db_file 
from ..tasks.generic_parse_imported_db_file import init_task__generic_parse_imported_db_file
from ..tasks.ad_populate_beatmap_sets import init_task__populate_beatmap_sets
from ..tasks.ae_populate_beatmaps import init_task__populate_beatmaps
from ..tasks.afa_populate_collections import init_task__populate_collections
from ..tasks.afb_populate_collection_items import init_task__populate_collection_items
from ..tasks.ag_populate_scores import init_task__populate_scores


def full_import():
    with SessionMaker() as session:
        run_job__osu_db_file_import(session)
        run_job__collection_db_file_import(session)
        run_job__scores_db_file_import(session)


def run_job__osu_db_file_import(session: Session):
        db_file_type = utils.osu_db_file_name
        db_file_path = utils.OSU_DB_FILE_PATH

        job = Job('job__osu_db_file_import')
        job.to_execute = [
            init_task__generic_import_db_file(
                db_file_type=db_file_type,
                db_file_path=db_file_path,
                force_refresh=False,
            ),
            init_precheck__table_exists(engine=engine, table='state'),
            init_task__generic_update_state_db_file(
                session=session,
                db_file_type=db_file_type,
                db_file_path=db_file_path,
                force_refresh=False,
            ),
            init_task__generic_parse_imported_db_file(
                session=session,
                db_file_type=db_file_type,
                force_refresh=False,
            ),            
            init_task__populate_beatmap_sets(session=session, force_refresh=False),
            init_task__populate_beatmaps(session=session, force_refresh=False),
        ]
        job.run()


def run_job__collection_db_file_import(session: Session):
        db_file_type = utils.collection_db_file_name
        db_file_path = utils.COLLECTION_DB_FILE_PATH

        job = Job('job__collection_db_file_import')
        job.to_execute = [
            init_task__generic_import_db_file(
                db_file_type=db_file_type,
                db_file_path=db_file_path,
                force_refresh=False,
            ),
            init_precheck__table_exists(engine=engine, table='state'),
            init_task__generic_update_state_db_file(
                session=session,
                db_file_type=db_file_type,
                db_file_path=db_file_path,
                force_refresh=False,
            ),
            init_task__generic_parse_imported_db_file(
                session=session,
                db_file_type=db_file_type,
                force_refresh=False,
            ),
            init_task__populate_collections(session, force_refresh=False),
            init_task__populate_collection_items(session, force_refresh=False),
        ]
        job.run()


def run_job__scores_db_file_import(session: Session):
        db_file_type = utils.scores_db_file_name
        db_file_path = utils.SCORES_DB_FILE_PATH

        job = Job('job__score_db_file_import')
        job.to_execute = [
            init_task__generic_import_db_file(
                db_file_type=db_file_type,
                db_file_path=db_file_path,
                force_refresh=False,
            ),
            init_precheck__table_exists(engine=engine, table='state'),
            init_task__generic_update_state_db_file(
                session=session,
                db_file_type=db_file_type,
                db_file_path=db_file_path,
                force_refresh=False,
            ),
            init_task__generic_parse_imported_db_file(
                session=session,
                db_file_type=db_file_type,
                force_refresh=False,
            ),
            init_task__populate_scores(session, force_refresh=False)
        ]
        job.run()
