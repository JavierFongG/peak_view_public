import os 
from sqlalchemy import create_engine, Column, Integer, String, Float 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session 
from dotenv import load_dotenv

load_dotenv() 

username = os.getenv("USERNAME") 
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base() 

Base.metadata.create_all(bind = engine)

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close() 