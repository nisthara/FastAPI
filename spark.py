from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
import csv
import pandas as pd

spark = SparkSession \
    .builder \
    .appName("Spark session") \
    .getOrCreate()

df = pd.read_csv('exported_csv.csv')
df.to_parquet('output.parquet')
# file = open(exported_csv.csv)
# type(file)
# csvreader = csv.reader(file)

# file.close()