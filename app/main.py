from fastapi import FastAPI 
from sqlalchemy.orm import Session 
from  utils.database import get_db 
import utils.models as models, utils.database as database
from routers import sales

app = FastAPI() 

models.Base.metadata.create_all(bind = database.engine)

app.include_router(sales.router, prefix = "/sales", tags = ["invoices"])

@app.get("/")
def root():
    return {'message' : 'im alive'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)