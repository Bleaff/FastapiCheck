from enum import Enum
import requests
# from sqlalchemy import create_engine
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
import psycopg2

db_name = 'quest_db'
db_user = 'check'
db_pass = '1111'
db_host = 'db'
db_port = '5432'

# Connecto to the database
# db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
# db = create_engine(db_string)

# def add_new_row(id, question, answer, created_at):
#     # Insert a new number into the 'numbers' table.
#     db.execute("INSERT INTO quest (id, question, answer, creadet_at) "+\
#         "VALUES (" + f'{id}, {question}, {answer}, {created_at});')

# def check_in_table(id):
#     db.execute(
#         f"select exists(select 1 from quest where id={id})"
#     )
#     return db.fetchone()

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



app = FastAPI()
#Just parse data to table
@app.get("/")
async def get_model(question_num : int):
    res = requests.get(f'https://jservice.io/api/random?count={question_num}')
    raw_json = res.json()
    parsed = list()
    for it in raw_json:
        parsed.append(Question.parse_obj(it))
    return parsed
    # return check_in_table(parsed[0].id)

    