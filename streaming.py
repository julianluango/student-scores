from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# =======================================================
##Crear sesión Spark en modo local
# =======================================================
spark = SparkSession.builder \
    .appName("KafkaTrafficStreaming") \
    .master("local[*]") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-traffic-checkpoint") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# =======================================================
##Esquema de los datos esperados del productor
# =======================================================
schema = StructType([
    StructField("city", StringType()),
    StructField("vehicle_type", StringType()),
    StructField("count", IntegerType()),
    StructField("timestamp", DoubleType())
])

# =======================================================
##Leer datos desde Kafka
# =======================================================
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic-data") \
    .option("startingOffsets", "latest") \
    .load()

# =======================================================
##Parsear el valor JSON
# =======================================================
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(F.from_json(F.col("value"), schema).alias("data")) \
    .select("data.*")

# =======================================================
##Procesamiento: total de vehículos por ciudad y tipo
# =======================================================
traffic_stats = parsed_df.groupBy("city", "vehicle_type").agg(
    F.sum("count").alias("total_vehicles")
)

# =======================================================
##Mostrar resultados en tiempo real
# =======================================================
query = traffic_stats.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime="5 seconds") \
    .start()

print("Streaming iniciado. Esperando datos desde Kafka...")

query.awaitTermination()
