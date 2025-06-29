from fastapi import APIRouter, APIRouter, Depends
from app.sql import schemas, database, product_crud
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, FileResponse
import base64
import uuid
import os
import logging

router = APIRouter()
router = APIRouter(prefix = '/products',tags=['Product'])

def product_data_db():
    db = database.SessionLocal()
    try:
        yield db

    finally:
        db.close()


@router.get("/")
# async def Get_Error_Data(db:Session = Depends(error_data_db)):
async def Get_Products(db:Session = Depends(product_data_db), product_name: str = None):
    
    try:
        logging.info(product_name)

        product_info = schemas.ProductSchemas(
            id = None,
            name = product_name
        )

        product_datas = product_crud.Get_Product_Data(db, product_info)

        if product_datas == None:
            return JSONResponse({'data':[], 'message':'OK'}, 200)


        return_list = []

        for product in product_datas:
            resp = schemas.ProductSchemas(
                id = str(product.id),
                name =  product.name,
                platformer = product.platformer,
                production_used = product.production_used,
                type = product.type,
                purchase_price = product.purchase_price,
                selling_price = product.selling_price,
                img_path = product.img_path,
                count = product.count
            )

            return_list.append(dict(resp))

        return JSONResponse({'data':return_list, 'message':'OK'}, 200)

    except Exception as err:
        logging.info(err)
        return JSONResponse({'data':[], 'message':'Server Error'}, 500)


@router.post("/")
async def Add_Products(db:Session = Depends(product_data_db), product_data: schemas.ProductSchemas = None):
    
    try:
        
        logging.info("Insert a new product data into database.")

        product_id = str(uuid.uuid4())

        file_extension = "png"        
        filename = f"{product_id}.{file_extension}"

        #save img file
        if product_data.img_base64 != None:
            filepath = f"./app/img/{filename}"
            save_img_result = save_img_file(product_data.img_base64, filepath)
            
            if save_img_result == False:
                return JSONResponse({'data':None, 'message':'Server Error'}, 500)

        db_data = product_crud.Add_new_Product_Data(db, product_id, filename, product_data)

        resp = schemas.ProductSchemas(
            id = product_id,
            name =  db_data.name,
            platformer = db_data.platformer,
            production_used = db_data.production_used,
            type = db_data.type,
            purchase_price = db_data.purchase_price,
            selling_price = db_data.selling_price,
            img_path = filename,
            count = db_data.count
        )

        return_data = dict(resp)

        logging.info("Insert a new product data into database success.")
        return JSONResponse({'data':return_data,'message':'OK'}, 201)

    except Exception as err:
        logging.info("Insert a new product data into database error.")
        logging.info(err)
        return JSONResponse({'data':None, 'message':'Server Error'}, 500)


@router.put("/")
async def Edit_Products(db:Session = Depends(product_data_db), product_data: schemas.ProductSchemas = None):

    try:
        logging.info("Edit the product data in the database.")

        #save img file
        if product_data.img_base64 != None:
            file_extension = "png"        
            filename = f"{product_data.id}.{file_extension}"
            filepath = f"./app/img/{filename}"

            save_img_result = save_img_file(product_data.img_base64, filepath)
            
            if save_img_result == False:
                return JSONResponse({'data':None, 'message':'Server Error'}, 500)

        db_data = product_crud.Edit_Product_Data(db, product_data)

        resp = schemas.ProductSchemas(
            id = db_data.id,
            name =  db_data.name,
            platformer = db_data.platformer,
            production_used = db_data.production_used,
            type = db_data.type,
            purchase_price = db_data.purchase_price,
            selling_price = db_data.selling_price,
            img_path = db_data.img_path,
            count = db_data.count
        )

        return_data = dict(resp)

        logging.info("Edit the product data in the database success.")

        return JSONResponse({'data':return_data, 'message':'OK'}, 200)
    
    except Exception as err:
        logging.info("Edit the product data in the database error.")
        logging.info(err)

        return JSONResponse({'data':None, 'message':'Server Error'}, 500)


@router.delete("/")
async def delete_product(db:Session = Depends(product_data_db), product_data: schemas.ProductInfoBase = None):

    logging.info("Delete the product data in the database.")

    try:
        
        delete_file_path = f"./app/img/{product_data.id}.png"

        # Delete the img file
        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)
        
        else:
            logging.info("The image file is not found.")
        
        db_data = product_crud.Delete_Product_Data(db, product_data)

        if db_data == None:
            return JSONResponse({'data':None, 'message':'Not find the deleted data in the database.'}, 400)
        
        else:
            logging.info("Delete the product data in the database suceess.")
            return JSONResponse({'data':dict(product_data), 'message':'OK'}, 200)
    
    except Exception as err:
        logging.info("Delete the product data in the database error.")
        logging.info(err)

        return JSONResponse({'data':None, 'message':'Server Error'}, 500)


def save_img_file(img_base64, filepath):

    try:
        prefix = img_base64.split(",")[0] + ","
        base64_string = img_base64.replace(prefix, "")
        image_data = base64.b64decode(base64_string)

        with open(filepath, "wb") as f:
            f.write(image_data)

        logging.info("Save the image file success.")

        return True

    except Exception as err:
        logging.info("Save the image file error.")
        logging.info(err)

        return False

@router.get("/get-image/{img_name}")
async def get_img(img_name:str):
    img_path = f"./app/img/{img_name}"
    return FileResponse(img_path)


@router.get("/test-image")
async def get_img():
    img_path = f"./app/img/test.jpeg"
    return FileResponse(img_path)