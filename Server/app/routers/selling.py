from fastapi import APIRouter, APIRouter, Depends
from app.sql import schemas, database, selling_crud, product_crud
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, FileResponse
import uuid
import logging
from datetime import datetime, timedelta

router = APIRouter()
router = APIRouter(prefix = '/selling',tags=['Selling'])

def selling_data_db():
    db = database.SessionLocal()
    try:
        yield db

    finally:
        db.close()


@router.get("/")
# async def Get_Error_Data(db:Session = Depends(error_data_db)):
async def Get_Selling_Record(db:Session = Depends(selling_data_db), start_date: str = None, end_date: str = None):
    
    try:
        
        logging.info(start_date)
        logging.info(end_date)

        if start_date == None or end_date == None:

            now_date = datetime.now()

            if start_date == None:
                temp_start_date = now_date + timedelta(days = -30)
                start_date = temp_start_date.strftime("%Y-%m-%d")
            
            if end_date == None:
                end_date = now_date.strftime("%Y-%m-%d")

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")


        selling_datas = selling_crud.Get_Selling_Data(db, start_date, end_date)

        if selling_datas == None:
            return JSONResponse({'data':[], 'message':'OK'}, 200)


        return_list = []
        
        for selling_data in selling_datas:
            return_date = selling_data.data_time.isoformat()
            resp = schemas.SellingSchemas(
                record_id = selling_data.record_id,
                id = selling_data.id,
                name =  selling_data.name,
                platformer = selling_data.platformer,
                production_used = selling_data.production_used,
                type = selling_data.type,
                purchase_price = selling_data.purchase_price,
                real_selling_price = selling_data.real_selling_price,
                sell_count = selling_data.sell_count,
                income = selling_data.income,
                data_time = return_date
            )

            return_list.append(dict(resp))

        return JSONResponse({'data':return_list, 'message':'OK'}, 200)

    except Exception as err:
        logging.info(err)
        return JSONResponse({'data':[], 'message':'Server Error'}, 500)


@router.post("/")
# async def Get_Error_Data(db:Session = Depends(error_data_db)):
async def Add_Selling_Record(db:Session = Depends(selling_data_db), selling_list_string:schemas.SellingListSchemas = None):
    
    try:
        
        logging.info(selling_list_string.selling_list)

        selling_list = eval(selling_list_string.selling_list)

        logging.info(type(selling_list))

        check_result, error_product_name, error_type = check_selling_data(selling_list)
        if check_result == False:
            return JSONResponse({'data':error_product_name, 'message':error_type}, 400)

        success_list = []

        for selling in selling_list:
            insert_result = selling_crud.Add_new_selling_Product_Data(db, selling)

            if insert_result == True:
                update_count = int(selling["count"]) - int(selling["sell_count"])
                update_count_result = product_crud.Update_Product_Count(db, selling["id"], update_count)

                if update_count_result == True:
                    success_list.append(selling)

        return JSONResponse({'data':success_list, 'message':'OK'}, 200)
    

    except Exception as err:
        logging.info(err)
        return JSONResponse({'data':[], 'message':'Server Error'}, 500)


def check_selling_data(selling_list):

    try:
        
        check_result = True
        error_product_name = ""
        error_type = ""

        for selling in selling_list:

            if selling["sell_count"] == "":
                check_result = False
                error_product_name = selling["name"]
                error_type = "Error Selling Count"
                break

            if int(selling["count"]) < int(selling["sell_count"]):
                check_result = False
                error_product_name = selling["name"]
                error_type = "Error Count"
                break

            if selling["real_selling_price"] == "":
                check_result = False
                error_product_name = selling["name"]
                error_type = "Error Selling Price"
                break
                
        return check_result, error_product_name, error_type
    
    except Exception as err:
        logging.info("Check the selling list data has error.")
        logging.info(err)

        return False
