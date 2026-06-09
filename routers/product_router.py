from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import database_models

from database import get_db
from schemas import Product

router = APIRouter()

@router.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


@router.get("/product/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
    return db.query(database_models.Product).filter(database_models.Product.id == id).first()


@router.post("/product")
def add_product(product: Product,db: Session = Depends(get_db)):
    db.add(
        database_models.Product(
            **product.model_dump()
        )
    )

    db.commit()

    return {"message": "Added"}