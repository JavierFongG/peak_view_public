from fastapi import FastAPI, Depends, Query, APIRouter
from sqlalchemy.orm import Session 
from database import get_db
from models import Invoices, Employee, CreditNotes
from routers import sales, payments, employees
import models, database

app = FastAPI() 

models.Base.metadata.create_all(bind=database.engine)

app.include_router(employees.router, prefix="/employees", tags = ["Employees"])
app.include_router(sales.router, prefix="/sales", tags = ["Invoices"])

@app.get("/")
def home(db: Session = Depends(get_db)): 
    return {'message' : 'im alive'}

# GET sales/seller/id 
# GET sales/product/id 
# GET sales/


# GET payments/seller/id 
# GET payments/payee/id 
# GET payments/ 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
