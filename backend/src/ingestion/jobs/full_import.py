from sqlalchemy.orm import Session

from src.common.db import engine, SessionMaker

from orchestrator import Job

import src.common.utils as utils

from ..prechecks.tables import init_precheck__table_exists
from ..prechecks.tables import init_precheck__state_table_populated

from ..tasks.generic_import_db_file import init_task__generic_import_db_file 
from ..tasks.generic_update_state_db_file import init_task__generic_update_state_db_file 
from ..tasks.generic_parse_imported_db_file import init_task__generic_parse_imported_db_file

from ..tasks.ad_populate_beatmapsets import init_task__populate_beatmapsets
from ..tasks.ad_populate_beatmapsets_api import init_task__populate_beatmapsets_api
from ..tasks.ae_populate_beatmaps import init_task__populate_beatmaps
from ..tasks.ae_populate_beatmaps_api import init_task__populate_beatmaps_api
from ..tasks.ah_populate_star_ratings import init_task__populate_beatmap_star_ratings
from ..tasks.ah_populate_star_ratings_api import init_task__populate_beatmap_star_ratings_api

from ..tasks.afa_populate_collections import init_task__populate_collections
from ..tasks.afb_populate_collection_items import init_task__populate_collection_items

from ..tasks.ag_populate_scores import init_task__populate_scores
from ..tasks.ag_populate_scores_api import init_task__populate_scores_api


def full_import(user_id: int):
    with SessionMaker() as session:
        # run_job__osu_db_file_import(session)
        # run_job__collection_db_file_import(session)
        # run_job__scores_db_file_import(session)
        run_job__api_import(user_id, session)


def run_job__api_import(user_id: int, session: Session):
    job = Job('job__osu_db_file_import')
    job.to_execute = [
        init_task__populate_beatmapsets_api(session=session, force_refresh=False),
        init_task__populate_beatmaps_api(session=session, force_refresh=False),
        init_task__populate_beatmap_star_ratings_api(session=session, force_refresh=False),
        init_task__populate_scores_api(user_id=user_id, session=session, force_refresh=False),
    ]
    job.run()


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
            init_task__populate_beatmapsets(session=session, force_refresh=False),
            init_task__populate_beatmaps(session=session, force_refresh=False),
            init_task__populate_beatmap_star_ratings(session=session, force_refresh=False),
            # init_task__populate_beatmap_star_ratings_advanced(session=session, force_refresh=False),
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
