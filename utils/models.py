from utils.database import Base 
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    issued_at = Column(DateTime)
    invoice_number = Column(String, nullable=False)
    subtotal = Column(Float)
    extra_discount = Column(Float)
    total = Column(Float)
    due = Column(Float)
    seller_id = Column(Integer, ForeignKey("employees.id"))
    payee_id = Column(Integer, ForeignKey("payees.id"))
    voided = Column(Boolean, default=False)

    seller = relationship("Employee", back_populates="invoices")
    payee = relationship("Payee", back_populates="invoices")
    details = relationship("InvoiceDetail", back_populates="invoice")
    credit_note = relationship("CreditNote", uselist=False, back_populates="invoice")


class InvoiceDetail(Base):
    __tablename__ = "invoice_details"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Float)
    unit_price = Column(Float)

    invoice = relationship("Invoice", back_populates="details")
    item = relationship("Item", back_populates="invoice_details")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    invoices = relationship("Invoice", back_populates="seller")


class Payee(Base):
    __tablename__ = "payees"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tin = Column(String)

    invoices = relationship("Invoice", back_populates="payee")


class CreditNote(Base):
    __tablename__ = "credit_notes"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    date = Column(Date)

    invoice = relationship("Invoice", back_populates="credit_note")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    invoice_details = relationship("InvoiceDetail", back_populates="item")
