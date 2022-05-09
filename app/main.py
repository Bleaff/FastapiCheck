from enum import Enum
import requests
# from sqlalchemy import create_engine
from fastapi import FastAPI
from pydantic import BaseModel

class Category(BaseModel):
    id           : int = None
    title        : str = None
    created_at   : str = None
    updated_at   : str = None
    clues_count  : int = None

class Question(BaseModel):
    id              : int = None
    answer          : str = None
    question        : str = None
    value           : int = None
    airdate         : str = None
    created_at      : str = None
    updated_at      : str = None
    category_id     : int = None
    game_id         : int = None
    invalid_count   : int = None
    category        : Category = None
# def pull_data():
#     engine = create_engine('postgresql+psycopg2://postgres:docker@172.17.0.2/my-db')
#     engine.connect()
#     print(engine)

app = FastAPI()
#Just parse data to table
@app.get("/")
async def get_model(question_num : int):
    res = requests.get(f'https://jservice.io/api/random?count={question_num}')
    raw_json = res.json()
    parsed = list()
    for it in raw_json:
        parsed.append(Question.parse_obj(it))
    # pull_data()
    return parsed

    