from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, IntegerType
from tenacity import retry, stop_after_attempt, wait_fixed

# Initialize Oracle client (ensure the library path is correct)
cx_Oracle.init_oracle_client(lib_dir="/oracle/instantclient_23_7")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Kafka-PySpark-Integration") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Kafka configuration
kafka_bootstrap_servers = "kafka_b:9094"
kafka_topic = "interaction"

# Define schema for JSON parsing
schema = StructType() \
    .add("id_client", IntegerType()) \
    .add("id_formation", IntegerType())

# Read data from Kafka
kafka_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Extract and parse JSON data
kafka_data = kafka_stream.selectExpr("CAST(value AS STRING) as json_string")
parsed_data = kafka_data.withColumn("data", from_json(col("json_string"), schema)) \
    .select("data.*")  # Extract `id_client` and `id_formation`

# Custom logic (if needed)
def custom_logic(df):
    # Add any additional transformations here
    return df

# Apply custom logic
processed_data = custom_logic(parsed_data)

# Retry logic for Oracle writes
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def insert_row(cursor, row):
    cursor.execute("""
        INSERT INTO HISTORY_SEARCH (id_client, id_formation, DATE_TIME_SEARCH)
        VALUES (:1, :2, CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Paris')
    """, (row.id_client, row.id_formation))

# Write to Oracle using foreachPartition for distributed execution
def write_to_oracle(batch_df, batch_id):
    def process_partition(rows):
        dsn = cx_Oracle.makedsn("host.docker.internal", 1521, service_name="XEPDB1")
        connection = cx_Oracle.connect(user="SEFORMER", password="153300", dsn=dsn)
        cursor = connection.cursor()
        try:
            for row in rows:
                insert_row(cursor, row)
            connection.commit()
        except Exception as e:
            print(f"Erreur lors de l'écriture dans Oracle : {e}")
        finally:
            cursor.close()
            connection.close()

    batch_df.foreachPartition(process_partition)

# Start the streaming query
query = processed_data.writeStream \
    .foreachBatch(write_to_oracle) \
    .outputMode("append") \
    .start()

# Wait for the streaming query to terminate
query.awaitTermination()