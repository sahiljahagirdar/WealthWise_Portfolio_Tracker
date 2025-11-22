from pydantic import BaseModel,Field
from typing import Annotated

class PriceBase(BaseModel):
    symbol: str
    price: float

class PriceCreate(PriceBase):
    pass

class PriceResponse(PriceBase):
    model_config = {'from_attributes': True}
