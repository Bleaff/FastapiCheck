from enum import Enum
import requests
# from sqlalchemy import create_engine
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, MetaData, Integer, Computed
import psycopg2

db_name = 'quest_db'
db_user = 'check'
db_pass = '1111'
db_host = 'db'
db_port = '5432'

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

def add_new_row(id, question, answer, created_at):
    # Insert a new number into the 'numbers' table.
    insert_string = "INSERT INTO quest (id, question, answer, created_at) VALUES " + f"({id}, %s, %s, %s);"
    db.execute(insert_string, (question, answer, created_at))

def check_in_table(id):
    result = db.execute(
        f"select exists(select 1 from quest where id={id})"
    )
    for (r) in result:  
        return r[0]

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




def get_request(q_num):
    res = requests.get(f'https://jservice.io/api/random?count={q_num}')
    raw_json = res.json()
    parsed = list()
    for it in raw_json:
        parsed.append(Question.parse_obj(it))
    return parsed

def get_unique_request():
    parsed = get_request(1)
    while check_in_table(parsed[0].id):
        parsed = get_request(1)
    return parsed[0].id, parsed[0].question, parsed[0].answer, parsed[0].created_at


app = FastAPI()
#Just parse data to table
@app.get("/")
async def get_model(question_num : int):
    res = requests.get(f'https://jservice.io/api/random?count={question_num}')
    raw_json = res.json()
    for it in raw_json:
        last = Question.parse_obj(it)
        if check_in_table(last.id):
            last = get_unique_request()
            add_new_row(last[0], last[1], last[2], last[3])
        else:
            add_new_row(last.id , last.question, last.answer, last.created_at)    
    return last

@app.get("/selected")
async def get_table_info():
    with db.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(str("select * from quest;"))
        res_list = list()
        for it in result:
            res_list.append(it)
    return res_list
