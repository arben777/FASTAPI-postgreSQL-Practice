from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Creates all the tables and columns in postgres

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_db():             # creates a connection to the database 
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/questions/{question_id}")
async def read_question(question_id: int, db:db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
            raise HTTPException(status_code=404, details= 'Question is not found')
    return result

@app.get("/choice/{question_id}")
async def read_choices(question_id, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
            raise HTTPException(status_code=404, details= 'Question is not found')
    return result

@app.post("/questions/")
async def create_questions(question: QuestionBase, db:db_dependency):  # The Question Base is the type from the pydantic model for data validation purposes 
# so we are passing in a data validation that is validating the body of the API request, the question
# and we are able to create a conenction to our database from our fastAPI application
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct,question_id = db_question.id)
        db.add(db_choice)
    db.commit()

# This is our API endpoint