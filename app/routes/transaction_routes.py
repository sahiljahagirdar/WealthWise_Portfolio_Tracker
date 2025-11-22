from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from decimal import Decimal
from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter(prefix='/transactions', tags=['Transactions'])

# Route to add Financial Transaction
@router.post('/')
def update_holdings(txn: TransactionCreate, db: Session = Depends(get_db)) -> dict:
    symbol = txn.symbol.upper()

    # Check existing User
    user_exists_query = text('SELECT * FROM users WHERE id = :uid')
    user = db.execute(user_exists_query, {"uid": txn.user_id}).fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail='User Not found')

    # Fetch existing holding
    query = text("SELECT * FROM holdings WHERE user_id = :uid AND symbol = :symbol")
    holding = db.execute(query, {"uid": txn.user_id, "symbol": symbol}).fetchone()
    
    # Convert floats to Decimal
    txn_units = Decimal(str(txn.units))
    txn_price = Decimal(str(txn.price))
    
    # ======================
    # UPDATE HOLDINGS LOGIC
    # ======================
    if holding:
        # BUY
        if txn.type.upper() == "BUY":
            total_cost_before = holding.units * holding.avg_cost
            total_cost_new = txn_units * txn_price
            new_units = holding.units + txn_units
            new_avg_cost = (total_cost_before + total_cost_new) / new_units
            
            update_query = text("""
                UPDATE holdings
                SET units = :units, avg_cost = :avg_cost
                WHERE id = :hid
            """)
            db.execute(update_query, {
                "units": new_units,
                "avg_cost": new_avg_cost,
                "hid": holding.id
            })
            db.commit()
        
        # SELL
        elif txn.type.upper() == "SELL":
            if holding.units < txn_units:
                raise HTTPException(status_code=400, detail="Not enough units to sell")
            
            new_units = holding.units - txn_units
            
            update_query = text("""
                UPDATE holdings
                SET units = :units
                WHERE id = :hid
            """)
            db.execute(update_query, {
                "units": new_units,
                "hid": holding.id
            })
            db.commit()

    else:
        # If holding doesn't exist
        if txn.type.upper() == "SELL":
            raise HTTPException(status_code=400, detail="You have no units to sell")
        
        insert_query = text("""
            INSERT INTO holdings (user_id, symbol, units, avg_cost)
            VALUES (:uid, :symbol, :units, :avg_cost)
        """)
        db.execute(insert_query, {
            "uid": txn.user_id,
            "symbol": symbol,
            "units": txn_units,
            "avg_cost": txn_price
        })
        db.commit()

    # Store all the transaction into transaction table [BUY/SELL]
    insert_txn_query = text("""
        INSERT INTO transactions (user_id, symbol, type, units, price,date)
        VALUES (:user_id, :symbol, :type, :units, :price, :date)
    """)

    db.execute(insert_txn_query, {
        "user_id": txn.user_id,
        "symbol": symbol,
        "type": txn.type.upper(),
        "units": float(txn_units),
        "price": float(txn_price),
        "date" : txn.date
    })
    db.commit()

    # Return success response
    return {
        "message": "Transaction processed successfully",
        "user_id": txn.user_id,
        "symbol": symbol,
        "type": txn.type.upper(),
        "units": float(txn_units),
        "price": float(txn_price)
    }


@router.get('/history', response_model=list[TransactionResponse])
def get_history(user_id: int, db: Session = Depends(get_db)):
    history_query = text('SELECT * FROM transactions WHERE user_id = :uid')
    history = db.execute(history_query, {"uid": user_id}).fetchall()
    if not history:
        raise HTTPException(status_code=404, detail='Transaction Not found')
    return history
