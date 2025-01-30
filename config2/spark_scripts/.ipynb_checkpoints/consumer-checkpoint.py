from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, IntegerType
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir="/oracle/instantclient_23_7") 

# Initialiser la session Spark
spark = SparkSession.builder \
    .appName("Kafka-PySpark-Integration") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Kafka configuration
kafka_bootstrap_servers = "kafka_b:9094"
kafka_topic = "interaction"

# Définir le schéma pour le parsing JSON
schema = StructType() \
    .add("id_client", IntegerType()) \
    .add("id_formation", IntegerType())

# Lire les données depuis Kafka
kafka_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Extraire et parser les données JSON
kafka_data = kafka_stream.selectExpr("CAST(value AS STRING) as json_string")

parsed_data = kafka_data.withColumn("data", from_json(col("json_string"), schema)) \
    .select("data.*")  # Extraire les champs `id_client` et `id_formation`

# ** Logique personnalisée : Traiter les données **
def custom_logic(df):
    # Vous pouvez ajouter ici des transformations supplémentaires si nécessaire
    return df

# Appliquer la logique personnalisée
processed_data = custom_logic(parsed_data)

# ** Écrire dans Oracle Database via cx_Oracle **
def write_to_oracle(batch_df, batch_id):
    # Initialiser le client Oracle
     # Chemin vers Oracle Instant Client

    # Détails de connexion Oracle
    dsn = cx_Oracle.makedsn("host.docker.internal", 1521, service_name="XEPDB1")
    connection = cx_Oracle.connect(user="SEFORMER", password="153300", dsn=dsn)

    try:
        cursor = connection.cursor()

        # Insérer les données dans Oracle
        for row in batch_df.collect():
            cursor.execute("""
                INSERT INTO HISTORY_SEARCH (id_client, id_formation, DATE_TIME_SEARCH)
                VALUES (:1, :2, CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Paris')
            """, (row.id_client, row.id_formation))
        
        # Valider la transaction
        connection.commit()
    except Exception as e:
        print(f"Erreur lors de l'écriture dans Oracle : {e}")
    finally:
        # Fermer la connexion
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Démarrer la requête de streaming
query = processed_data.writeStream \
    .foreachBatch(write_to_oracle) \
    .outputMode("append") \
    .start()

# Attendre la fin du streaming
query.awaitTermination()