from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from database import get_db
from models import Employee

router = APIRouter() 

@router.get("/")
def get_employees(db: Session = Depends(get_db)): 
    return db.query(Employee).all() 