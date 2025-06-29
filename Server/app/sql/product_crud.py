from sqlalchemy.orm import Session
from app.sql import models, schemas, database
from fastapi.encoders import jsonable_encoder
import logging

#  Get device error data
def Get_Product_Data(db:Session, product_info:schemas.ProductSchemas):

    logging.info("Get the data from the database.")
    try:
        data = db.query(models.Products)

        if data is None: 
            return None
        
        logging.info("Get the data from the database success.")
        return data

    except Exception as err:
        logging.info("Get the data from the database fail.")
        logging.info(err)
        return None 


def Add_new_Product_Data(db:Session, product_id:str, save_img_path:str, product_info:schemas.ProductSchemas):

    logging.info("Add a new product data in the database.")
    try:
        db_product_info = models.Products(
            id = product_id,
            name = product_info.name,
            platformer = product_info.platformer,
            production_used = product_info.production_used,
            type = product_info.type,
            purchase_price = product_info.purchase_price,
            selling_price = product_info.selling_price,
            img_path = save_img_path,
            count = product_info.count
        )

        db.add(db_product_info)
        db.commit()
        logging.info("Add new data in the database success.")
        return db_product_info
    
    except Exception as err:
        logging.info("Add new data in the database fail.")
        logging.info(err)

        return None


def Edit_Product_Data(db:Session, product_info:schemas.ProductSchemas):

    logging.info("Edit the product data in database.")

    try:

        product_db_data = db.query(models.Products).filter(models.Products.id == product_info.id).first()

        product_db_data.name = product_info.name
        product_db_data.platformer = product_info.platformer
        product_db_data.production_used = product_info.production_used
        product_db_data.type = product_info.type
        product_db_data.purchase_price = product_info.purchase_price
        product_db_data.selling_price = product_info.selling_price
        product_db_data.count = product_info.count

        db.commit()

        updated_data = db.query(models.Products).filter(models.Products.id == product_info.id).first()

        logging.info("Edit the product data in database success.")

        return updated_data
    
    except Exception as err:
        logging.info("Edit the product data in database fail.")
        logging.info(err)

        return None


def Delete_Product_Data(db:Session, product_info:schemas.ProductInfoBase):
    logging.info("Delete the product data in database.")

    try:
        db_product_data = db.get(models.Products, product_info.id)

        if db_product_data is None:
            return None
        
        else:
            db.delete(db_product_data)
            db.commit()
            logging.info("Delete the product data in the database success.")

            return jsonable_encoder(db_product_data)
            
    except Exception as err:
        logging.info("Delete the product data in the database fail.")
        logging.info(err)

        return None
    

def Update_Product_Count(db:Session, product_id:str, update_count:int):
    logging.info("Update the product count data in database.")

    try:
        product_db_data = db.query(models.Products).filter(models.Products.id == product_id).first()

        product_db_data.count = update_count
        db.commit()

        return True

    except Exception as err:
        logging.info("Update the product count data in database error.")
        logging.info(err)
        return False