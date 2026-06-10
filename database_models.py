from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Float,Boolean,DateTime
from datetime import datetime, timezone
Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description=Column(String)
    price=Column(Float)
    quantity=Column(Integer)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String,default="user")
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
