from json import load
from sqlalchemy import create_engine, Column, String, Integer 
from sqlalchemy.orm import sessionmaker, declarative_base 
from pyspark.sql import SparkSession
from sqlalchemy.inspection import inspect
import tables
import sys
import os
import urllib
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=localhost;"
                                 "DATABASE=estdb;"
                                 "UID=sa;"
                                 "PWD=estuate@123")
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
print("mssql+pyodbc:///?odbc_connect={}".format(params))
conn = engine.connect()
tables.Base.metadata.create_all(engine)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self) -> str:
        return f"< id = {self.id}, name = {self.name}, address = {self.password}, email = {self.email}>"
    def dict(self):
        return {"id" : self.id, "name" : self.name, "adress" : self.password, "email" : self.email}

db = SessionLocal()

os.environ["spark_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2"
os.environ["hadoop_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2\\bin\\Hadoop"
os.environ["path"] += f";{os.environ['hadoop_home']}\\bin"
os.environ["pyspark_python"] = "C:\\Users\\Nisthara\\myenv\\Scripts\\Python"

spark = SparkSession \
    .builder \
    .appName("Spark session") \
    .getOrCreate()

df = spark.read.option('header','true').csv('exported_csv.csv')
df.show()


result = db.query(Employees).all()
print(result)
result_list = []
for customer in result:
        result_list.append(customer.dict())

if not result_list:
    print("The list is empty")
    sys.exit(1)
else:
    print(result_list)
    pass
df = spark.createDataFrame(result_list)
df.show()
df.write.mode("overwrite").option('compression','snappy').parquet('exported_parquet.parquet')
# file = open(exported_csv.csv)
# type(file)
# csvreader = csv.reader(file)

# file.close()











# async def write_data(user:User):
#         return [connection.execute(users.insert().values(id=user.id,name=user.name,email=user.email,password=user.password)),
#         connection.execute(users.select()).fetchall(),
#         {"message":"succesfull"}]
        