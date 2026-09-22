# from src.ingestion.jobs.full_import import run_job__full_import

# from src.level_browser.db import Model, engine
# from src.level_browser.models.beatmaps import BeatmapSet, Beatmap

# Model.metadata.drop_all(engine)
# Model.metadata.create_all(engine)

# run_job__full_import()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.query.api import router as beatmaps_router


app = FastAPI()

app.include_router(beatmaps_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {'message': 'Hello World'}
