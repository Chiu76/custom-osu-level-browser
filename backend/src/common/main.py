from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.beatmap_query.api import router as beatmap_query_router
from src.api.grouping_query.api import router as grouping_query_router
from src.api.score_query.api import router as score_query_router


app = FastAPI()

app.include_router(beatmap_query_router)
app.include_router(grouping_query_router)
app.include_router(score_query_router)

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
