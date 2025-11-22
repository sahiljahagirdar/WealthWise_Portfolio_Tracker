from pydantic import BaseModel,Field
from typing import Annotated

class HoldingSummary(BaseModel):
    symbol : Annotated[str,Field(...,description='Ticket symbol of the holding',examples=['TCS'])]
    units : Annotated[float,Field(...,description='Total units held by the user',examples=[5])]
    avg_cost : Annotated[float,Field(...,description='Weighted average cost per unit')]
    current_price : Annotated[float,Field(...,description='Latest market price for the holding',examples=[3400])]
    unrealized_pl : Annotated[float,Field(...,description='Profit/Loss for the holding',examples=[1000])]

    model_config = {"from_attributes":True}


class PortfolioSummary(BaseModel):
    user_id : Annotated[int,Field(...,description='User ID whose portfolio is returned',examples=[1])]
    holdings : Annotated[list[HoldingSummary],Field(...,description='List og the holdings with detailed profit/loss')]
    total_value : Annotated[float,Field(...,description='Total market value of all holdings')]
    total_gain : Annotated[float,Field(...,description='Total unrealized gain accross entire portfolio')]