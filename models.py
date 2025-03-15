from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Enum, Float
from pydantic import BaseModel 
from database import Base 

class Invoices(Base): 
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

class Employee(Base): 
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class CreditNotes(Base): 
    __tablename__ = "credit_notes"
    id = Column(Integer, primary_key = True)
    date = Column(String) 
    total = Column(Float)
    invoice_id = Column(Integer)
    employee_id = Column(Integer)
    payer_id = Column(Integer)

