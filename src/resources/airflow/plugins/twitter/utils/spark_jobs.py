import sys
import json
from pyspark.sql import SparkSession


spark = SparkSession.builder.getOrCreate()
dataframe = spark.createDataFrame(json.loads(sys.argv[1]))
dataframe.write.save(format=sys.argv[3], path=sys.argv[2], mode=sys.argv[3])
