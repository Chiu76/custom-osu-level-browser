from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.beatmap_query.api import router as beatmap_query_router


app = FastAPI()

app.include_router(beatmap_query_router)

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
