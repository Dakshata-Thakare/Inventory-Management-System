from fastapi import FastAPI,Depends
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()
database_models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
products = [
    Product(id=11, name="Phone", description="Budget smartphone", price=99.99, quantity=50),
    Product(id=21, name="Laptop", description="Gaming laptop", price=999.99, quantity=10),
    Product(id=31, name="Headphones", description="Wireless headphones", price=59.99, quantity=100),
    Product(id=41, name="Keyboard", description="Mechanical keyboard", price=79.99, quantity=30),
    Product(id=51, name="Mouse", description="Wireless mouse", price=29.99, quantity=75),
    Product(id=61, name="Monitor", description="24-inch Full HD monitor", price=149.99, quantity=20),
    Product(id=71, name="Tablet", description="10-inch Android tablet", price=199.99, quantity=15),
    Product(id=81, name="Smartwatch", description="Fitness tracking smartwatch", price=89.99, quantity=40),
    Product(id=91, name="Speaker", description="Bluetooth speaker", price=49.99, quantity=60),
    Product(id=101, name="Power Bank", description="20000mAh power bank", price=34.99, quantity=80),
]

def init_db():
    db = session()
    count = db.query(database_models.Product).count
    if count ==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    
        db.commit()

init_db()

@app.get("/")
def greet():
    # print("Welcome...")
    return "Welcome........."

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    # return "Getting all the products"
    db_products  = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return "product not found"
    # return products[id-1]

@app.post("/product")
def add_product(product:Product,db:Session = Depends):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    # products.append(product)
    return "Successfully added"

@app.put("/product/{id>}")
def update_product(id:int,product:Product,db:Session = Depends):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.quantity = product.quantity
        db_product.price = product.price
        db.commit()
        return "Successfullly Updated.."
    # for i in range(len(products)):
    #     if products[i].id ==id:
    #         products[i] = product
    #         return "Product Added Successfully"
    return "No Product Found"


@app.delete("/product/{id}")
def delete_product(id:int,db:Session = Depends):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted Successfully"

    # for i in range(len(products)):
    #     if products[i].id ==id:
    #         del products[i]
    #         return "Product deleted Successfully"
    return "No Product Found"