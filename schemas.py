#this model for pydantic
from pydantic import BaseModel

class Product(BaseModel):
    id:int
    name:str
    description:str
    price:float
    quantity:int

    #pydantic automatically validate the incoming req hence no need to add manual validatio
    # def __init__(self,id:int,name:str,description:str,price:float,quantity:int):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity =quantity

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserInDB(User):
    hashed_password: str
