import os

DB_ADDRESS = 'db'
DB_USER_NAME = os.environ.get('DB_USER_NAME')
with open('/run/secrets/db_password') as f:
    DB_PASSWORD = f.read()
DB_DATABASE_NAME = os.environ.get('DB_DATABASE_NAME')
WEB_PORT = 8000

import sys
import requests
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, inspect, Column, Integer, String, DateTime, desc
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
import uvicorn

app = FastAPI()

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_DATABASE_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False, unique=True)
    answer = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False)
    date_added = Column(DateTime, server_default=func.now(), nullable=False)

class NewQuestionsRequest(BaseModel):
    questions_num: int

def get_new_questions(db: SessionLocal, questions_num: int):
    questions_added: int = 0
    while questions_added < questions_num:
        response = requests.get(f'https://jservice.io/api/random?count={questions_num - questions_added}')
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail='Failed to get questions from API')
        for row in response.json():
            if db.query(Question).filter(Question.question == row['question']).first():
                continue
            question = Question(question=row['question'], answer=row['answer'], date_created=row['created_at'])
            db.add(question)
            db.commit()
            questions_added += 1

@app.post('/new-questions/')
async def new_questions_handler(request: NewQuestionsRequest):
    db = SessionLocal()
    try:
        return_value: Dict = {}
        row = db.query(Question).order_by(Question.id.desc()).first()
        if row:
            return_value = {'id': row.id, 'question': row.question, 'answer': row.answer,
                            'date_created': row.date_created, 'date_added': row.date_added}
        get_new_questions(db, request.questions_num)
        return return_value
    except HTTPException as e:
        print(f'({sys.exc_info()[-1].tb_lineno}) {type(e).__name__}: {e}')
        raise
    except Exception as e:
        print(f'({sys.exc_info()[-1].tb_lineno}) {type(e).__name__}: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')
    finally:
        db.close()

if __name__ == '__main__':
    if not inspect(engine).has_table('question'):
        Base.metadata.create_all(bind=engine)
    # uvicorn.run('main:app', host='0.0.0.0', port=WEB_PORT, reload=True)
    uvicorn.run(app, host='0.0.0.0', port=WEB_PORT)
