from pyspark.sql import SparkSession
import csv
import pandas as pd

spark = SparkSession \
    .builder \
    .appName("Spark session") \
    .getOrCreate()

df = spark.read.option('header','true').csv('exported_csv.csv')
df.show()
df.write.option('compression','snappy').parquet('exported_parquet.parquet')

# file = open(exported_csv.csv)
# type(file)
# csvreader = csv.reader(file)
# file.close()
