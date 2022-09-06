from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from pyspark.sql import SparkSession
import inspect
import sys
import os
import urllib
import tables

params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=localhost;"
                                 "DATABASE=estdb;"
                                 "UID=sa;"
                                 "PWD=estuate@123")
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
SessionLocal = sessionmaker(bind=engine)

def get_dict(obj : tables.Base):
    fields = dict(vars(obj))
    del fields["_sa_instance_state"]
    return fields
db = SessionLocal()
for cls_obj, cls_name in inspect.getmembers(sys.modules["tables"]):
    if inspect.isclass(cls_obj):
        print(cls_name)
# print(tables)
# result = db.query(tables.Employees).all()
# result_list = list(map(get_dict, result))
# pprint.pprint(result_list)