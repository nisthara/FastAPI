from multiprocessing import connection
from config import config
from connection import create_engine 
from sqlalchemy.orm import decl_api, sessionmaker
import urllib, os, subprocess, colorama, importlib, sys, inspect
from pyspark.sql import SparkSession
from fastapi import HTTPException
from typing import List

colorama.init(autoreset=True)
os.environ["spark_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2"
os.environ["hadoop_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2\\bin\\Hadoop"
os.environ["path"] += f";{os.environ['hadoop_home']}\\bin"
os.environ["pyspark_python"] = "C:\\Users\\Nisthara\\myenv\\Scripts\\Python"

spark = SparkSession.builder.appName("Local Creator").getOrCreate()

def get_dict(obj: decl_api.DeclarativeMeta):
    fields = dict(vars(obj))
    del fields["_sa_instance_state"]
    return fields

def create_parquet(engine, schemas:List[str], tablename:List[str]=[], path:str="dest", compression:str="snappy"):
    for schema in schemas:
        details = config.connection_details
        params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"+
                                    f"SERVER={details.ip_address};"
                                    f"DATABASE={details.database_name};"
                                    f"UID={details.username};"
                                    f"PWD={details.password}")
        url = "{}+{}:///?odbc_connect={}".format(details.database_type,"pyodbc", params)
        print(colorama.Fore.GREEN+"INFO:","\t  Connection URL : ",url)
        engine = create_engine(url)
        SessionLocal = sessionmaker(bind=engine)
        sqla_path = "C:\\Users\\Nisthara\\myenv\\Scripts\\sqlacodegen.exe"
        print(colorama.Fore.GREEN+"INFO:",f"\t  Running Command : {sqla_path} {url} --outfile {schema}.py")
        subprocess.Popen([sqla_path, url, "--outfile", f"{schema}.py"]).wait()
        table_module = importlib.__import__(schema)
        importlib.reload(table_module)
        print(colorama.Fore.GREEN+"INFO:",f"\t  Removing file : {schema}.py")
        os.remove(f"{schema}.py")
        if not tablename:
            tables = [cls_obj for _cls_name, cls_obj in inspect.getmembers(sys.modules[schema]) if inspect.isclass(cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base"]
            for table in tables:
                db = SessionLocal()    
                result = db.query(table).all()
                result = list(map(get_dict, result))
                try:
                    df = spark.createDataFrame(result)
                    print(colorama.Fore.GREEN+"INFO:",f"\t  Writing {table.__name__} to {path} using {compression}")
                    df.repartition(1).write.mode("overwrite").format("parquet").option("compression", compression).save(f"{path}/{table.__name__}")
                except ValueError:
                    raise HTTPException(status_code=500, detail=f"Cannot infer Column Datatypes for Table {table.__name__} Please provide the schema manually.")
        else:
            tables = [cls_obj for _cls_name, cls_obj in inspect.getmembers(sys.modules[schema]) if inspect.isclass(cls_obj) and isinstance(cls_obj, decl_api.DeclarativeMeta) and cls_obj.__name__ != "Base" and cls_obj.__tablename__ in tablename]
            for table in tables:
                db = SessionLocal()    
                result = db.query(table).all()
                result = list(map(get_dict, result))
                try:
                    df = spark.createDataFrame(result)
                    print(colorama.Fore.GREEN+"INFO:",f"\t  Writing {table.__name__} to {path} using {compression}")
                    df.repartition(1).write.mode("overwrite").format("parquet").option("compression", compression).save(f"{path}/{table.__name__}")
                except ValueError:
                    raise HTTPException(status_code=500, detail=f"Cannot infer Column Datatypes for Table {table.__name__}, Please provide the schema manually.")
        del table_module