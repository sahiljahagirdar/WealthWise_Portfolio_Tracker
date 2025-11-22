from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.price import PriceCreate, PriceResponse

router = APIRouter(prefix="/prices",tags=['Prices'])

# Route responsible for performing Symbol ADD and UPDATE into DB
@router.post('/', response_model=PriceResponse)
def add_or_update_price(request: PriceCreate, db:Session = Depends(get_db)):

    # Convert the symbol to Upper
    symbol = request.symbol.upper()


    # Query to filter user symbols to Database stores symbols
    price_entry_query = text('SELECT * FROM prices where symbol = :symbol')
    price_entry = db.execute(price_entry_query,{"symbol":symbol}).fetchone()

    # If symbol exists in the DB Update the existing price
    if price_entry:
        previous_price = price_entry.price
        update_price_query = text("""
            UPDATE prices
            SET price = :price
            WHERE symbol = :symbol
            RETURNING *
        """)

        updated_price = db.execute(update_price_query, {
            "price": request.price,
            "symbol": symbol
        }).fetchone()

        db.commit()
        return dict(updated_price._mapping)

    # If symbol does not exists create new one 
    else:
        insert_price_query = text("""
            INSERT INTO prices (price, symbol)
            VALUES (:price, :symbol)
            RETURNING *
        """)

        new_price = db.execute(insert_price_query, {
            "price": request.price,
            "symbol": symbol
        }).fetchone()

        db.commit()
        return dict(new_price._mapping)

@router.get('{symbol}',response_model=PriceResponse)
def get_prices(symbol:str, db:Session = Depends(get_db)):
    symbol = symbol.upper()

    # Query to find user symbol inside DB
    price_entry_query = text('SELECT * from prices where symbol = :symbol')
    price_entry = db.execute(price_entry_query,{"symbol":symbol}).fetchone()

    # If symbol exists return the symbol and price
    if price_entry:
        return price_entry
    else:
        raise HTTPException(status_code=404, detail='Price not found') # Error is symbol does not exists
    

# Route to get all prices of the available symbols
@router.get('/all', response_model=list[PriceResponse])
def get_all_prices(db:Session = Depends(get_db)):
    all_price_query = text('SELECT * FROM prices')
    all_price = db.execute(all_price_query)
    return all_price