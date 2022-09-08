import inspect
import os
import urllib
import tables
import sys
import connection
from connection import engine
from fastapi import FastAPI, Form
from sqlalchemy import create_engine, inspect as inspect_engine
from sqlalchemy.orm import sessionmaker, decl_api
from pyspark.sql import SparkSession

app = FastAPI()

app.include_router(connection.router)

#connection
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                     "SERVER=localhost;"
                                     "DATABASE=estdb;"
                                     "UID=sa;"
                                     "PWD=estuate@123")
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
conn = engine.connect()
tables.Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

#spark credentials
os.environ["spark_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2"
os.environ["hadoop_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2\\bin\\Hadoop"
os.environ["path"] += f";{os.environ['hadoop_home']}\\bin"
os.environ["pyspark_python"] = "C:\\Users\\Nisthara\\myenv\\Scripts\\Python"

#sparksession
spark = SparkSession.builder.appName("Data Archiver").getOrCreate()

#dict convertion
def get_dict(obj: tables.Base):
    fields = dict(vars(obj))
    del fields["_sa_instance_state"]
    return fields

#creating a table instance
table = [cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules["tables"]) if inspect.isclass(
    cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]

#connection to database
@app.get("/")
@connection.connection_required
def index():
    return {"detail": "Hello World"}

#retriving schemas
@app.get('/schema_name')
def get_schema():
    inspector = inspect_engine(engine)
    schema_name = inspector.get_schema_names()
    return schema_name

#retriving table names
@app.get('/table_name')
def get_table():
    inspector =  inspect_engine(engine)
    table_name = inspector.get_table_names()
    return table_name

#retriving columns
@app.get('/{table}')
def get_columns(table:str):
    inspector = inspect_engine(engine)
    col_name = inspector.get_columns(table)
    return col_name

#creating a data frame and converting it into parquet files at  
#distinct destinations for each table that is present in the datebase 
