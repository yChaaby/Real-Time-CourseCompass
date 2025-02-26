from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Kafka-PySpark-Integration") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Read data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka_b:9094") \
    .option("subscribe", "interaction") \
    .load()

# Process data
processed_df = df.selectExpr("CAST(value AS STRING) as message")

# Write data to console
query = processed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()