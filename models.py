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