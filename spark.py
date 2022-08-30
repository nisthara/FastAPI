from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession

# engine=None
# server = 'localhost,1433' # to specify an alternate port
# database = 'estdb' 
# username = 'sa' 
# password = 'estuate@123'
# params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
#                                  "SERVER=localhost;"
#                                  "DATABASE=estdb;"
#                                  "UID=sa;"
#                                  "PWD=estuate@123")
# print(params)                                 
# engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
# print("mssql+pyodbc:///?odbc_connect={}".format(params))
# connection=engine.connect()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

spark = SparkSession \
    .builder \
    .appName("Spark session") \
    .getOrCreate()