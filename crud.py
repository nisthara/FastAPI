from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi import FastAPI, Form
import urllib
engine=None

#connection
server = 'localhost,1433' # to specify an alternate port
database = 'estdb' 
username = 'sa' 
password = 'estuate@123'
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=localhost;"
                                 "DATABASE=estdb;"
                                 "UID=sa;"
                                 "PWD=estuate@123")
print(params)                                 
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
print("mssql+pyodbc:///?odbc_connect={}".format(params))
connection=engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

meta = MetaData()
users= Table(
    'employees',
    meta,
    Column('id', Integer,primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('password', String(255)))
meta.create_all(engine)

#schema
class User(BaseModel):
    id:int 
    name:str    
    email:str
    password:str
      
app =FastAPI()

@app.post("/login")
async def login(server: str = Form() ,database: str = Form() ,username: str = Form(), password: str = Form() ):
    # server = server # to specify an alternate port
    # database = database 
    # username = username
    # password = password
    # params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 # "SERVER=localhost;"
                                 # "DATABASE=estdb;"
                                 # "UID=sa;"
                                 # "PWD=estuate@123")
    # engine = create_engine("mssql+pyodbc://sa:estuate@123@localhost:1433/estdb")
    # connection=engine.connect()

    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base = declarative_base()
    return {"connection": "achieved"}

@app.get("/")
async def read_data():
    stmt = users.select()
    return connection.execute(stmt).fetchall()
    pass 
    
@app.get("/{id}")
async def read_data(id:int):
        return connection.execute(users.select().where(users.c.id==id)).fetchall()
       
@app.post("/")
async def write_data(user:User):
        return [connection.execute(users.insert().values(id=user.id,name=user.name,email=user.email,password=user.password)),
        connection.execute(users.select()).fetchall(),
        {"message":"succesfull"}]
        
@app.put("/{id}")
async def update_data(id:int,user:User):
    connection.execute(users.update().values(
         name=user.name,
         email=user.email,
         password=user.password).where(users.c.id==id))
    return connection.execute(users.select()).fetchall()        

@app.delete("/{id}")
async def delete_data(id:int):
    connection.execute(users.delete().where(users.c.id == id))
    return connection.execute(users.select()).fetchall()        
    
#ins = company_table.insert().values(id='7',name='ram', department='HR')
#result = connection.execute(ins)