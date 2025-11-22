from pydantic import BaseModel, Field
from datetime import date
from typing import Annotated, Literal

class TransactionBase(BaseModel):
    user_id: Annotated[int, Field(..., description="ID of the user performing the transaction", examples=[1])]
    symbol: Annotated[str, Field(..., description='Stock or asset ticker symbol', examples=['TCS'])]
    type: Annotated[Literal['BUY', 'SELL'], Field(..., description='Operation type', examples=['BUY'])]
    units: Annotated[float, Field(..., description='Number of units purchased or sold')]
    price: Annotated[float, Field(..., description='Price per unit during the transaction', examples=[3200])]
    date: Annotated[date, Field(..., description='Date when the transaction happened')]


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: Annotated[int, Field(..., description='Auto-generated transaction ID', examples=[101])]

    model_config = {'from_attributes': True}
