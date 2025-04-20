# spark_streaming.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, from_unixtime
from pyspark.sql.types import StructType, IntegerType, DoubleType, LongType

print ('Beginning...')

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()
print ('builder...')

spark.sparkContext.setLogLevel("WARN")
print ('setLogLevel...')

schema = StructType() \
    .add("sensor_id", IntegerType()) \
    .add("temperature", DoubleType()) \
    .add("timestamp", LongType())
print ('Schema is created.')

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "sensor-data") \
    .load()
print ('Read Streaming is completed')

df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")
print ('DF parsing is completed')

# Агрегация: средняя температура по каждому сенсору за окно 10 секунд
df_parsed_ts = df_parsed.withColumn("event_time", from_unixtime(col("timestamp")).cast("timestamp"))

agg = df_parsed_ts \
    .withWatermark("event_time", "1 minute") \
    .groupBy(
        col("sensor_id"),
        window(col("event_time"), "10 seconds")
    ).avg("temperature")
print ('Aggregation is completed')

query = agg.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", False) \
    .start()
print ("What's else?...")

query.awaitTermination()
print ('End.')
