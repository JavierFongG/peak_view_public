from fastapi import FastAPI 
from sqlalchemy.orm import Session 
from models import Invoice
from database import get_db 
import models, database
from routers import sales

app = FastAPI() 

models.Base.metadata.create_all(bind = database.engine)

app.include_router(sales.router, prefix = "/sales", tags = ["invoices"])

@app.get("/")
def root():
    return {'message' : 'im alive'}