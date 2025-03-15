from fastapi import FastAPI, Request
import asyncio
from typing import Optional
import os  

app = FastAPI()

@app.get("/")
async def home():
    return "Hello, World!"

@app.get("/name")
async def name_route(name: Optional[str] = "Unknown"):
    return f"Hello, {name}!"

@app.get("/env_vars") 
async def env_test(): 
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    database = os.getenv("DATABASE")

    return {
        "USER" : username 
        , "PASSWORD" : password
        , "HOST" : host
        , "PORT" : port 
        , "DB" : database 
    }

@app.post("/post-data")
async def post_data(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)