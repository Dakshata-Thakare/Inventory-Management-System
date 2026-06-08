from fastapi import FastAPI
import database_models
from database import engine
from routers.auth_router import router as auth_router
from routers.product_router import router as product_router

app = FastAPI()

database_models.Base.metadata.create_all(
    bind=engine
)

app.include_router(auth_router)
app.include_router(product_router)


@app.get("/")
def greet():
    return {
        "message": "Welcome"
    }