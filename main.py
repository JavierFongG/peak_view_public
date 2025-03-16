from fastapi import FastAPI 
from sqlalchemy.orm import Session 
from  app.utils.database import get_db 
import app.utils.models as models, app.utils.database as database
from app.routers import sales

app = FastAPI() 

models.Base.metadata.create_all(bind = database.engine)

app.include_router(sales.router, prefix = "/sales", tags = ["invoices"])

@app.get("/")
def root():
    return {'message' : 'im alive'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)