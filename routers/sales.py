from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Invoice, InvoiceDetail, Employee, Payee, CreditNote, Item, Bundle, ItemCategory
from sqlalchemy import text, func, not_, exists, case
import pandas as pd
from datetime import datetime 


router = APIRouter() 

@router.get("/")
def sales_root(): 
    return {"message": "Sales router working"}

@router.get("/details")
def sales_detail(db: Session = Depends(get_db)):
    result = (
        db.query(
            Invoice.date,
            func.date(Invoice.issued_at).label("issued_at"),
            CreditNote.date.label("creditnote_date"),
            Invoice.invoice_number,
            Invoice.subtotal,
            Invoice.extra_discount,
            Invoice.total,
            Invoice.due,
            Invoice.seller_id,
            Employee.name.label("seller_name"),
            Invoice.payee_id,
            Payee.name.label("payee_name"),
            Payee.tin.label("payee_nit"), 
            InvoiceDetail.item_id,
            case(
                (InvoiceDetail.item_id.isnot(None), InvoiceDetail.item_id),
                (InvoiceDetail.bundle_id.isnot(None), InvoiceDetail.bundle_id)
            ).label("itemd_id"),
            Item.name.label("item_name"),
            case(
                (InvoiceDetail.item_id.isnot(None), Item.name),
                (InvoiceDetail.bundle_id.isnot(None), Bundle.name)  # Replace 'Bundle Name' with the actual bundle name logic if available
            ).label("item_name"),
            case(
                (ItemCategory.name.isnot(None), ItemCategory.name),
                else_="unknown"
            ).label("item_category"),
            InvoiceDetail.quantity.label("item_quantity"),
            InvoiceDetail.unit_price.label("item_unitprice"),
            (InvoiceDetail.quantity * InvoiceDetail.unit_price * (1 - (Invoice.extra_discount / Invoice.subtotal))).label("item_sales")
        )
        .join(InvoiceDetail, Invoice.id == InvoiceDetail.invoice_id)
        .join(Employee, Invoice.seller_id == Employee.id)
        .join(Payee, Invoice.payee_id == Payee.id)
        .outerjoin(CreditNote, (Invoice.id == CreditNote.invoice_id) & (not_(CreditNote.voided)))
        .outerjoin(Item, InvoiceDetail.item_id == Item.id)
        .outerjoin(Bundle, InvoiceDetail.bundle_id == Bundle.id)
        .outerjoin(ItemCategory, Item.item_category_id == ItemCategory.id)
        .filter(Invoice.voided == False)
        .filter(Invoice.invoice_number.isnot(None))
        .filter(Invoice.invoice_number != '')  # Added condition to remove invoice_number = ''
        .all()
    )

    # Convert query results into JSON serializable format
    return [
        {
            "date": row.date,
            "issued_at": row.issued_at,
            "creditnote_date": row.creditnote_date,
            "invoice_number": row.invoice_number,
            "subtotal": row.subtotal,
            "extra_discount": row.extra_discount,
            "total": row.total,
            "due": row.due,
            "seller_id": row.seller_id,
            "seller_name": row.seller_name,            
            "payee_id": row.payee_id,
            "payee_name": row.payee_name,
            "payee_nit": row.payee_nit,
            "item_id": row.item_id,
            "item_name": row.item_name,
            "item_category": row.item_category,
            "item_quantity": row.item_quantity,
            "item_unitprice": row.item_unitprice,
            "item_sales": row.item_sales
        }
        for row in result
    ]