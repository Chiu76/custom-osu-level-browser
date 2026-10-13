from typing import Literal

from sqlalchemy.orm import InstrumentedAttribute

from src.common.models.scores import Score


TOP_BY = Literal['accuracy', 'played_at']

TOP_BY_COLUMNS = {
    'accuracy': Score.accuracy,
    'played_at': Score.played_at,
}

def get_column__top_by(top_by: TOP_BY) -> InstrumentedAttribute:
    if top_by not in TOP_BY_COLUMNS.keys():
        raise ValueError(f'Received invalid top_by value, not present in `TOP_BY_COLUMNS` mapping: {top_by}')
    return TOP_BY_COLUMNS[top_by]
