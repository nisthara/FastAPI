from pyspark.sql import SparkSession
import os , sys
def read_file(path:str):
    os.environ["spark_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2"
    os.environ["hadoop_home"] = "C:\\Users\\Nisthara\\myenv\\spark-3.2.2-bin-hadoop3.2\\bin\\Hadoop"
    os.environ["path"] += f";{os.environ['hadoop_home']}\\bin"
    os.environ["pyspark_python"] = "C:\\Users\\Nisthara\\myenv\\Scripts\\Python"
    spark = SparkSession.builder.appName("Parquet Reader").getOrCreate()
    try:
        df = spark.read.parquet(sys.argv[1])
        df.show()
        df.printSchema()
        print("The total number of columns read form the archive : ", len(df.columns))
        print("The total number of rows read form the archive : ", df.count())
    except Exception as e:
        print(f"{e}")

read_file(sys.argv[1])