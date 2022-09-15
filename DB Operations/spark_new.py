import inspect, os, tables, sys, parquet, connection
from typing import List
from fastapi import FastAPI, HTTPException
from config import config
from sqlalchemy import create_engine, inspect as inspect_engine
from sqlalchemy.orm import decl_api
from pyspark.sql import SparkSession

#connection

app = FastAPI()

app.include_router(connection.router)

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
@connection.connection_required
def get_schema():
    inspector = inspect_engine(config.engine)
    schema_name = inspector.get_schema_names()
    return schema_name

#retriving table names
@app.get('/table_name')
@connection.connection_required
def get_table(schema:str):
    inspector =  inspect_engine(config.engine)
    table_name = inspector.get_table_names(schema)
    if not table_name:
        raise HTTPException(status_code=404, detail=f"No such schema found : {schema}")
    return table_name

#retriving columns 
@app.get('/{table}')
@connection.connection_required
def get_columns(table:str):
    try:
        inspector = inspect_engine(config.engine)
        col_name = inspector.get_columns(table)
        result = {}
        for row in col_name:
            result[row["name"]] = f'{row["type"]}'
        if result:
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    return {"message" : "No such table exists"}

#archiving the tables in the schema
@app.post('/archive_table')
@connection.connection_required
def archive(schemas:List[str], table:List[str]=[]):
    parquet.create_parquet(config.engine, schemas, table)
    return {"message":"done"}

#archiving the schemas in the database
@app.post('/archive_schema')
@connection.connection_required
def archive(schemas:List[str],compression:str):
    parquet.create_parquet(config.engine, schemas, compression)
    return {"message":"done"}

