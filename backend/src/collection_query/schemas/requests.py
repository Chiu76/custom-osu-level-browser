from pydantic import BaseModel


class CollectionQueryRow(BaseModel):
    collection_id: int
    name: str
    total_count: int
    selected_count: int


class CollectionQueryResponse(BaseModel):
    rows: list[CollectionQueryRow]
