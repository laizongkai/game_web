from sqlalchemy.orm import Session
from app.sql import models, schemas, database
from fastapi.encoders import jsonable_encoder
import logging
import uuid


def Get_Selling_Data(db:Session, start_date, end_date):
    logging.info(f"Get selling product data from {start_date} to {end_date}")
    try:
        data = db.query(models.Selling).filter(models.Selling.data_time < end_date, models.Selling.data_time >= start_date).all()
        return data
    
    except Exception as err:
        logging.info(f"Get selling product data from {start_date} to {end_date} fail.")
        logging.info(err)

        return None


def Add_new_selling_Product_Data(db:Session, selling:dict):

    # logging.info("Insert new selling product data into the database.")
    try:
        real_income = (int(selling["real_selling_price"]) - int(selling["purchase_price"])) * int(selling["sell_count"])

        db_product_info = models.Selling(
            record_id = str(uuid.uuid4()),
            id = selling["id"],
            name = selling["name"],
            platformer = selling["platformer"],
            production_used = selling["production_used"],
            type = selling["type"],
            purchase_price = selling["purchase_price"],
            real_selling_price = selling["real_selling_price"],
            sell_count = selling["sell_count"],
            income = real_income
        )

        db.add(db_product_info)
        db.commit()

        logging.info("Insert new selling product data into the database success.")
        return True
    
    except Exception as err:
        logging.info("Insert new selling product data into the database fail.")
        logging.info(err)

        return False