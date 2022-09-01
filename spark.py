from pyspark.sql import SparkSession
import csv

spark = SparkSession \
    .builder \
    .appName("Spark session") \
    .getOrCreate()

df = spark.read.option('header','true').csv('exported_csv.csv')
df.show()
df.write.option('compression','snappy').parquet('D:\dest')

# file = open(exported_csv.csv)
# type(file)
# csvreader = csv.reader(file)

# file.close()
