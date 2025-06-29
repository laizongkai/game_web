from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from app.sql.database import Base
from datetime import date, datetime

class Products(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key = True, index = True)
    name = Column(String, unique = True)
    platformer = Column(String)
    production_used = Column(String)
    type = Column(String)
    purchase_price = Column(Integer)
    selling_price = Column(Integer)
    img_path = Column(String, default = None)
    count = Column(Integer)


class Selling(Base):
    __tablename__ = "selling"
    
    record_id = Column(String, primary_key = True, index = True)
    id = Column(String)
    name = Column(String)
    platformer = Column(String)
    production_used = Column(String)
    type = Column(String)
    purchase_price = Column(Integer)
    real_selling_price = Column(Integer)
    sell_count = Column(Integer)
    income = Column(Integer)
    data_time = Column(Date, default = date.today())