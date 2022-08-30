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

df = spark.read.option('header','true').csv('exported_csv.csv')
df.show()

# file = open(exported_csv.csv)
# type(file)
# csvreader = csv.reader(file)

# file.close()