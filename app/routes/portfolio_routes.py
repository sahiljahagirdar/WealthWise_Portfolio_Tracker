from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.schemas.summary import PortfolioSummary, HoldingSummary

router = APIRouter(prefix="/portfolio-summary", tags=['Portfolio'])

@router.get('/',response_model=PortfolioSummary)
def get_portfolio_summary(user_id:int, db: Session = Depends(get_db)):

    user_query = text('SELECT * FROM USERS where id = :uid')

    user = db.execute(user_query,{"uid":user_id}).fetchone()

    if not user:
        raise HTTPException(status_code = 404, detail = 'User not found')
    
    holding_query = text('SELECT * from holdings where user_id = :uid')
    
    holdings = db.execute(holding_query,{"uid":user_id}).fetchall()

    if not holdings:
        return PortfolioSummary(
            user_id=user_id,
            holdings=[],
            total_value=0,
            total_gain=0
        )
    
    summary_list = []
    total_portfolio_value = 0
    total_unrealized_gain = 0

    for h in holdings:
        prince_entry_query = text('SELECT * from prices where symbol = :symbol')
        price_entry = db.execute(prince_entry_query,{"symbol":h.symbol}).fetchone()

        if not price_entry:
            raise HTTPException(status_code=404,detail=f'Price not found for {h.symbol}')
        
        current_price = price_entry.price 
        unrealized_pl = (current_price - h.avg_cost) * h.units

        total_value = h.units * current_price

        summary_list.append(HoldingSummary(
            symbol= h.symbol,
            units = h.units,
            avg_cost = h.avg_cost,
            current_price=current_price,
            unrealized_pl=unrealized_pl
        ))

        total_portfolio_value += total_value
        total_unrealized_gain += unrealized_pl

    return PortfolioSummary(
        user_id = user_id,
        holdings=summary_list,
        total_value=total_portfolio_value,
        total_gain=total_unrealized_gain
    )