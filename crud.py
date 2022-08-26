import urllib
from sqlalchemy import create_engine, MetaData, Table, Column, String
from typing import List
import pyodbc
from sqlalchemy.sql import select
import databases
import sqlalchemy
from fastapi import FastAPI, Form
from pydantic import BaseModel


#api to read the credentials
app = FastAPI()


@app.post("/login/")
async def login(sever: str = Form(), database: str = Form(), username: str = Form(), password: str = Form()):
    return {"username": username}



###connect
server = 'localhost,1433' # to specify an alternate port
database = 'estdb' 
username = 'sa' 
password = 'estuate@123'
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=localhost;"
                                 "DATABASE=estdb;"
                                 "UID=sa;"
                                 "PWD=estuate@123")
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
print(engine)


###create table
ob=MetaData()
con=engine.connect()
user = Table(
    "employee", 
    ob,
    Column('employee_id', String(30)),
    Column('employee_name', String(50)),
    Column('designation', String(40)),
    Column('age', String(10)))
ob.create_all(engine)
#print(user.columns.keys())


###insert
ins = user.insert().values(employee_id='13', employee_name='nisthara', designation='intern', age='21')
str(ins)
ins.compile().params
{"employee_id":'13', "employee_name":'nisthara', "designation":'intern', "age":'21'}
ins.bind=engine
con=engine.connect()
con
result = con.execute(ins)
#print(ins)

ins=user.insert()
con.execute=(ins,{"employee_id":'13', "employee_name":'nisthara', "designation":'intern', "age":'21'})
#print(ins)

###select
# s = select(user)
# result = con.execute(s)