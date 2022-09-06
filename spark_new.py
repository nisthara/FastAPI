from functools import wraps
from json import load
import os
import inspect
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, decl_api
from pyspark.sql import SparkSession
import tables
import urllib

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

#table object retrival from tables.py module
table = [cls_obj for cls_name, cls_obj in inspect.getmembers(sys.modules["tables"]) if inspect.isclass(
    cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]

#writing to parquet
for tab in table:
    print("---------------------------------------------------------------------")
    print("                         ", tab.__name__)
    print("---------------------------------------------------------------------")
    result = db.query(tab).all()
    if not result:
        continue
    result = list(map(get_dict, result))
    df = spark.createDataFrame(result)
    df.repartition(1).write.mode("overwrite").option("compression", "snappy").parquet(f"dest/{tab.__name__}")
