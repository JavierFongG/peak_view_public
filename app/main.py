from fastapi import FastAPI 
# from sqlalchemy.orm import Session 
from database import get_db 

app = FastAPI() 

@app.get("/")
def root():
    return {'message' : 'im alive'}