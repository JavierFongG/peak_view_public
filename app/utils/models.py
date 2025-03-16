from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Enum, Float
from pydantic import BaseModel 
from app.utils.database import Base 

class Invoice(Base): 
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String) 
    invoice_number = Column(String)
    date = Column(String)
    issued_at = Column(String)
    subtotal = Column(Float)
    total = Column(Float)
    due = Column(Float)
    taxable = Column(Integer)
    seller_id = Column(Integer)
    voided = Column(Boolean)