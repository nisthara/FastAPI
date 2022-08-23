from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/operations/{number1}/{number2}")
async def operations(number1:int,number2:int):
    if(number2==0):
        return {"Error":"Divide by zero error"}
    else:
        return {"Sum":number1+number2,"Difference":number1-number2, "Product":number1*number2, "quotient":number1/number2}