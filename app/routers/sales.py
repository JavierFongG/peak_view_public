from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from models import Invoices, CreditNotes
from sqlalchemy import text , func , not_, exists
import pandas as pd
from datetime import datetime 

router = APIRouter() 

@router.get("/")
def get_sales(db: Session = Depends(get_db)): 
    return db.query(Invoices).all()

@router.get("/overall")
def get_overall_sales(db: Session = Depends(get_db)):
    query = text("""
		select 
			i.issued_at 
			, p.id as client_id
			, e.id as seller_id 
			, it.id as item_id 
			, i.invoice_number 
			, max(p."name") as client_name 
			, max(e."name") as seller_name 
			, max(it."name") as item_name 
			, avg(case 
					when i.extra_discount > 0 then id.price * (1 - (i.extra_discount / i.subtotal))
					else id.price
			end)/4 as avg_item_selling_price
			, sum(id.quantity)*3 as sum_item_selling_quantity 
			, max(case when i.extra_discount > 0 then 1 else 0 end) as discounted_item
			, false as is_credit_note 
		from invoice_details id 
		left join invoices i on id.invoice_id = i.id 
		left join employees e on i.seller_id = e.id 
		left join payees p on i.payee_id = p.id 
		left join items it on id.item_id = it.id 
		where not i.voided  and i.invoice_number is not null
		group by 
			i.issued_at 
			, p.id 
			, e.id  
			, it.id  
			, i.invoice_number 
		union all 
		select 
			cn.date as issued_at 
			, p.id as client_id
			, e.id as seller_id 
			, it.id as item_id 
			, i.invoice_number 
			, max(p."name") as client_name 
			, max(e."name") as seller_name 
			, max(it."name") as item_name 
			, -1 * avg(case 
					when i.extra_discount > 0 then id.price * (1 - (i.extra_discount / i.subtotal))
					else id.price
			end) as avg_item_selling_price
			, -1 * sum(id.quantity) as sum_item_selling_quantity 
			, max(case when i.extra_discount > 0 then 1 else 0 end) as discounted_item
			, true as is_credit_note
		from invoice_details id 
		left join invoices i on id.invoice_id = i.id 
		left join employees e on i.seller_id = e.id 
		left join payees p on i.payee_id = p.id 
		left join items it on id.item_id = it.id 
		inner join credit_notes cn on i.id = cn.invoice_id 
		where not i.voided  and i.invoice_number is not null
		group by 
			cn.date 
			, p.id 
			, e.id  
			, it.id  
			, i.invoice_number 
	""")
    result = db.execute(query)
    return [dict(row._mapping) for row in result]

@router.get("/seller/detail")
def get_overall_sales(seller_id: int, start_date: str, end_date : str,db: Session = Depends(get_db)):
    query = text(f"""
		select 
			i.issued_at 
			, p.id as client_id
			, e.id as seller_id 
			, it.id as item_id 
			, i.invoice_number 
			, max(p."name") as client_name 
			, max(e."name") as seller_name 
			, max(it."name") as item_name 
			, avg(case 
					when i.extra_discount > 0 then id.price * (1 - (i.extra_discount / i.subtotal))
					else id.price
			end) as avg_item_selling_price
			, sum(id.quantity) as sum_item_selling_quantity 
			, max(case when i.extra_discount > 0 then 1 else 0 end) as discounted_item
			, false as is_credit_note 
		from invoice_details id 
		left join invoices i on id.invoice_id = i.id 
		left join employees e on i.seller_id = e.id 
		left join payees p on i.payee_id = p.id 
		left join items it on id.item_id = it.id 
		where not i.voided  and i.invoice_number is not null and e.id = {seller_id} and i.issued_at >= '{start_date}' and i.issued_at <= '{end_date}'
		group by 
			i.issued_at 
			, p.id 
			, e.id  
			, it.id  
			, i.invoice_number 
		union all 
		select 
			cn.date as issued_at 
			, p.id as client_id
			, e.id as seller_id 
			, it.id as item_id 
			, i.invoice_number 
			, max(p."name") as client_name 
			, max(e."name") as seller_name 
			, max(it."name") as item_name 
			, -1 * avg(case 
					when i.extra_discount > 0 then id.price * (1 - (i.extra_discount / i.subtotal))
					else id.price
			end) as avg_item_selling_price
			, -1 * sum(id.quantity) as sum_item_selling_quantity 
			, max(case when i.extra_discount > 0 then 1 else 0 end) as discounted_item
			, true as is_credit_note
		from invoice_details id 
		left join invoices i on id.invoice_id = i.id 
		left join employees e on i.seller_id = e.id 
		left join payees p on i.payee_id = p.id 
		left join items it on id.item_id = it.id 
		inner join credit_notes cn on i.id = cn.invoice_id 
		where not i.voided  and i.invoice_number is not null and e.id = {seller_id} and cn.date >= '{start_date}' and cn.date <= '{end_date}'
		group by 
			cn.date 
			, p.id 
			, e.id  
			, it.id  
			, i.invoice_number 
	""")
    result = db.execute(query)
    return [dict(row._mapping) for row in result]


@router.get("/seller/{seller_id}/{start_date}/{end_date}")
def get_sales(seller_id: int, start_date: str, end_date : str, db: Session = Depends(get_db)): 
    data = db.query(Invoices).filter_by(seller_id = seller_id).all()
    if len(data) == 0: 
        return {'message' : 'invalid ID'}
    return {'data' : data}
    
        # return  

# GET sales/product/{product_id}

# GET sales/bonus?seller_id={seller_id}&start_date={start_date}&end_date={end_date}
@router.get("/bonus")
def get_bonus(seller_id: int, start_date: str, end_date : str, db: Session = Depends(get_db)): 
    print(seller_id, start_date, end_date)
    query = text(f"""
    select 
		seller_name 
		, extract(year from created_at) as date_year 
		, extract(month from created_at) as date_month 
		, sum(invoice_amount_total) as invoice_amount_total
		, sum(case when is_taxable then invoice_amount_total * (1 - (1/1.12)) else 0 end) as invoice_tax
		, sum(case when is_taxable then invoice_amount_total * (1 - (1 - (1/1.12))) else 0 end) as net_sales 
        , sum(invoice_amount_total) - sum(invoice_amount_due) as paid_amount
		, sum(invoice_amount_due) as due_amount
        , case 
            when sum(invoice_amount_total) < 50000 then 0 
            when sum(invoice_amount_total) < 100000 then 0.015
            when sum(invoice_amount_total) < 150000 then 0.03
            when sum(invoice_amount_total) < 200000 then 0.04 
            when sum(invoice_amount_total) > 200000 then 0.05
        end perc_bonus 
        , case 
            when sum(invoice_amount_total) < 50000 then 0  
            when sum(invoice_amount_total) < 100000 then 0.015 
            when sum(invoice_amount_total) < 150000 then 0.03
            when sum(invoice_amount_total) < 200000 then 0.04 
            when sum(invoice_amount_total) > 200000 then 0.05
        end * sum(case when is_taxable then invoice_amount_total * (1 - (1 - (1/1.12))) else 0 end) total_bonus 
        , case 
            when sum(invoice_amount_total) < 50000 then 0  
            when sum(invoice_amount_total) < 100000 then 0.015 
            when sum(invoice_amount_total) < 150000 then 0.03
            when sum(invoice_amount_total) < 200000 then 0.04 
            when sum(invoice_amount_total) > 200000 then 0.05
        end * (sum(invoice_amount_total) - sum(invoice_amount_due)) over_paid_bonus 
	from (
		select 
			inv.id
			, inv.invoice_number 
			, inv."date" as created_at
			, inv.issued_at as issued_at
			, emp."name"  as seller_name 
			, inv.total as invoice_amount_total
			, inv.total - inv.due as invoice_amount_paid
			, inv.due as invoice_amount_due
			, inv.taxable as is_taxable
			from invoices inv 
			left join employees emp on inv.seller_id = emp.id
			where 
				not inv.voided -- No documentos Anulados  
				and inv.invoice_number is not NULL
                and inv.seller_id = {seller_id}
			union all 
			select 
				inv.id
				, inv.invoice_number 
				, cn."date" as created_at
				, inv.issued_at as issued_at
				, emp."name"  as seller_name 
				, -1 * inv.total as invoice_amount_total
				, 0 as invoice_amount_paid
				, 0 as invoice_amount_due
				, cn.taxable as is_taxable
			from invoices inv 
			left join employees emp on inv.seller_id = emp.id
			inner join credit_notes cn on inv.id = cn.invoice_id 	
            where inv.seller_id = {seller_id}
	) sq 
    where sq.issued_at >= '{start_date}' and sq.issued_at <= '{end_date}'
	group by 
		seller_name 
		, extract(year from created_at)  
		, extract(month from created_at)
	order by 
		seller_name
		, date_year 
		, date_month;
    """)
    result = db.execute(query)

    return [dict(row._mapping) for row in result]
    

@router.get("/summary")
def sales_summary(start_date = None,end_date = None, db: Session = Depends(get_db)):
    filters = []
    try: 
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            filters.append(Invoices.issued_at >= start_date)
        
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            filters.append(Invoices.issued_at <= end_date)

        
        if end_date and start_date:
            if end_date < start_date:
                return {'error' : 'Invalid date range'}
    
    except ValueError:
        
        return {'error' : 'Date format error'}
    
    # Removes invoice with credit notes 
    filters.append(
        not_(
            exists().where(
                CreditNotes.invoice_id == Invoices.id,
                CreditNotes.date >= start_date,  # Credit note date >= start_date
                CreditNotes.date <= end_date     # Credit note date <= end_date
            )
        )
    )

    # Removes voided invoices 
    filters.append(Invoices.voided == False)

    # Removes invoices with no invoice number 
    filters.append(Invoices.invoice_number.isnot(None))
    

    total_sales = db.query(func.sum(Invoices.total)).filter(*filters).scalar()
    
    return {'total_sales' : total_sales or 0.0}


@router.get("/growth")
def sales_growth(db: Session = Depends(get_db)):
    return {
        'current_sales' : 0
        , 'previous_sales' : 0
        , 'growth_percentage' : 0 
    }


@router.get("/products/top")
def sales_products_top(category, db: Session = Depends(get_db)):
    return [
        {"product" : "name", "units_sold": 0, "sale_amount": 0}
        , {"product" : "name", "units_sold": 0, "sale_amount": 0}
    ]


@router.get("/due")
def sales_due_payments(db: Session = Depends(get_db)): 
    return [
		{"invoice_number" : "abc123", "due_amount": 0, "expected_date": "2024-01-01"}
    ]


@router.get("/aov")
def sales_average_order_value(db: Session = Depends(get_db)): 
    return {"average_order_value" : 0}


@router.get("/monthly")
def sales_timeseries(start_date, end_date, db: Session = Depends(get_db)): 
    filters = []
    try: 
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            filters.append(Invoices.date >= start_date)
        
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            filters.append(Invoices.date <= end_date)

        
        if end_date and start_date:
            if end_date < start_date:
                return {'error' : 'Invalid date range'}
    
    except ValueError:
        
        return {'error' : 'Date format error'}
    
    # Removes invoice with credit notes 
    filters.append(
        not_(
            exists().where(
                CreditNotes.invoice_id == Invoices.id,
                CreditNotes.date >= start_date,  # Credit note date >= start_date
                CreditNotes.date <= end_date     # Credit note date <= end_date
            )
        )
    )

    # Removes voided invoices 
    filters.append(Invoices.voided == False)

    # Removes invoices with no invoice number 
    filters.append(Invoices.invoice_number.isnot(None))
    

    monthly_sales = db.query(
        func.date_trunc('month', Invoices.issued_at).label('month'),
        func.sum(Invoices.subtotal).label('total_sales')
    ).filter(*filters).group_by(func.date_trunc('month', Invoices.date)).all()
    
    # Format the result to a dictionary for easier reading
    result = [{"month": month.strftime('%Y-%m'), "total_sales": total_sales or 0.0} for month, total_sales in monthly_sales]

    return {"monthly_sales": result}


@router.get("/dates")
def sales_available_dates(db: Session = Depends(get_db)): 
    dates = db.query(
            func.min(Invoices.issued_at).label("min_date")
            , func.max(Invoices.issued_at).label("max_date")
    ).first() 

    min_date, max_date = dates 

    return {'min_date' : min_date , 'max_date' : max_date}