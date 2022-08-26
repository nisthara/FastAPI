#####basic working of fast api's
#from typing import Union

#from fastapi import FastAPI

#app = FastAPI()


#@app.get("/")
#def read_root():
 #   return {"Hello": "World"}

#path parameter 
#@app.get("/items/{item_id}")
#def read_item(item_id: int):
 #   return {"item_id": item_id}
    
 ###ordering of path parameter
#@app.get("/user/me")
#async def read_userme():
 #   return {"user_id":"current user"}
    
#@app.get("/user/{user_id}")
#async def read_userid(user_id:str):
 #   return {"User ID":user_id}
 
 
 
 
 ####enumulators
#from enum import Enum

#from fastapi import FastAPI


# class ModelName(str, Enum):
    # alexnet = "alexnet"
    # resnet = "resnet"
    # lenet = "lenet"


# app = FastAPI()


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
    # if model_name == ModelName.alexnet:
        # return {"model_name": model_name, "message": "Deep Learning FTW!"}

    # if model_name.value == "lenet":
        # return {"model_name": model_name, "message": "LeCNN all the images"}

    # return {"model_name": model_name, "message": "Have some residuals"}
    
    
    
    
    
 # from enum import Enum

# from fastapi import FastAPI


# class ModelName(str, Enum):
    # alexnet = "alexnet"
    # resnet = "resnet"
    # lenet = "lenet"


# app = FastAPI()


# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
    # if model_name == ModelName.alexnet:
        # return {"model_name": model_name, "message": "Deep Learning FTW!"}

    # if model_name.value == "lenet":
        # return {"model_name": model_name, "message": "LeCNN all the images"}

    # return {"model_name": model_name, "message": "Have some residuals"}
import urllib
from sqlalchemy import create_engine

server = 'localhost,1433' # to specify an alternate port
database = 'estdb' 
username = 'sa' 
password = 'estuate@123'

params = urllib.parse.quote_plus("'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password")

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
conn = engine.connect()