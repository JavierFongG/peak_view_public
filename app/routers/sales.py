from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from database import get_db

router = APIRouter() 

@router.get("/")
def sales_root(): 
    return {"message": "Sales router working"}

