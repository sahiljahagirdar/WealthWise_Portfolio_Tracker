from pydantic import BaseModel,Field
from typing import Annotated
class UserBase(BaseModel):
    name : Annotated[str, Field(description='Full name of the user',examples=['Sahil Jahagirdar'])]
    email : Annotated[str,Field(description='Email Id of the user',examples=['sahil@example.com'])]

class UserCreate(UserBase):
    pass 

class UserResponse(UserBase):
    id : Annotated[int,Field(description='Auto-Generated unique ID',examples=[1])]


    model_config = {"from_attributes": True}
