from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductInfoBase(BaseModel):
    id:Optional[str] = None
    name:Optional[str] = None

class ProductSchemas(ProductInfoBase):
    platformer:Optional[str]= None
    production_used:Optional[str] = None
    type:Optional[str] = None
    purchase_price:Optional[int] = None
    selling_price:Optional[int] = None
    img_path:Optional[str] = None
    img_base64:Optional[str] = None
    count:Optional[int] = None


class SellingListSchemas(BaseModel):
    selling_list:Optional[str] = None


class SellingSchemas(ProductInfoBase):
    record_id:Optional[str] = None

    platformer:Optional[str]= None
    production_used:Optional[str] = None
    type:Optional[str] = None
    purchase_price:Optional[int] = None
    real_selling_price:Optional[int] = None
    sell_count:Optional[int] = None
    income:Optional[int] = None
    data_time:Optional[str] = None
