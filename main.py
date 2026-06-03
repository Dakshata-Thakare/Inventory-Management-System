from fastapi import FastAPI
from models import Product
from database import session,engine
import database_models

app = FastAPI()
database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    # print("Welcome...")
    return "Welcome........."
products = [
    Product(id=1, name="Phone", description="Budget smartphone", price=99.99, quantity=50),
    Product(id=2, name="Laptop", description="Gaming laptop", price=999.99, quantity=10),
    Product(id=3, name="Headphones", description="Wireless headphones", price=59.99, quantity=100),
    Product(id=4, name="Keyboard", description="Mechanical keyboard", price=79.99, quantity=30),
    Product(id=5, name="Mouse", description="Wireless mouse", price=29.99, quantity=75),
    Product(id=6, name="Monitor", description="24-inch Full HD monitor", price=149.99, quantity=20),
    Product(id=7, name="Tablet", description="10-inch Android tablet", price=199.99, quantity=15),
    Product(id=8, name="Smartwatch", description="Fitness tracking smartwatch", price=89.99, quantity=40),
    Product(id=9, name="Speaker", description="Bluetooth speaker", price=49.99, quantity=60),
    Product(id=10, name="Power Bank", description="20000mAh power bank", price=34.99, quantity=80),
]

@app.get("/products")
def get_all_products():
    # return "Getting all the products"
    return products

@app.get("/product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    return "product not found"
    # return products[id-1]

@app.post("/product")
def add_product(product:Product):
    products.append(product)
    return "Successfully added"

@app.put("/product/{id>}")
def update_product(id:int,product:Product):
    for i in range(len(products)):
        if products[i].id ==id:
            products[i] = product
            return "Product Added Successfully"
    return "No Product Found"

@app.delete("/product/{id}")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id ==id:
            del products[i]
            return "Product deleted Successfully"
    return "No Product Found"