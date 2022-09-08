from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Package(BaseModel):
    name:str
    number:str
    desciption: Optional[str]= None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/operations/{number1}/{number2}")
async def operations(number1:int,number2:int):
    if(number2==0):
        return {"Error":"Divide by zero error"}
    else:
        return {"Sum":number1+number2,"Difference":number1-number2, "Product":number1*number2, "quotient":number1/number2}
        
        
        
@app.post("/package/{priority}")
async def make_pack(priority:int,package:Package,value:int):
    return {"priority":priority, **package.dict(),"value": value}