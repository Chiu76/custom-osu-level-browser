from src.common.db import engine, SessionMaker

from orchestrator import Job

from ..prechecks.tables import init_precheck__table_exists
from ..prechecks.tables import init_precheck__state_table_populated

from ..tasks.a_import_osu_db_file import init_task__import_osu_db_file 
from ..tasks.b_update_state_osu_db_file import init_task__update_state_osu_db_file
from ..tasks.c_parse_imported_osu_db_file import init_task__parse_imported_osu_db_file

from ..tasks.populate_beatmap_sets import init_task__populate_beatmap_sets
from ..tasks.populate_beatmaps import init_task__populate_beatmaps


def run_job__full_import():
    with SessionMaker() as session:
        job = Job('job__level_browser_full_import')
        job.to_execute = [
            init_task__import_osu_db_file(force_refresh=False),
            init_precheck__table_exists(engine=engine, table='state'),
            init_task__update_state_osu_db_file(session=session, force_refresh=False),
            init_task__parse_imported_osu_db_file(session=session, force_refresh=False),            
            init_task__populate_beatmap_sets(session=session, force_refresh=False),
            init_task__populate_beatmaps(session=session, force_refresh=False),
        ]
        job.run()
