# this is where we write our pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType
from pyspark.sql.functions import from_json, col
import os


#directory where Spark will store its checkpoint data. crucial in streaming to enable fault tolerance

checkpoint_dir = "tmp/checkpoint/kafka_to_postgres"
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)


postgres_config = {
    "url":"jdbc:postgresql://postgres:5432/stock_data",
    "user":"admin",
    "password":"admin",
    "dbtable":"stocks",
    "driver":"org.postgresql.Driver"
}


# The Schema/ Structure matching the new data coming from kafka
kafka_data_schema = StructType([
    StructField("date", StringType()),
    StructField("high", StringType()),
    StructField("low", StringType()),
    StructField("open", StringType()),
    StructField("close", StringType()),
    StructField("symbol", StringType())
])

spark = (SparkSession.builder
         .appName('kafkaSparkStreaming')
         .getOrCreate()
)

df = ( spark.readStream.format('kafka')
      .option('kafka.bootstrap.servers', 'kafka:9092')
      .option('subscribe', 'stock_analysis')
      .option('startingOffsets', 'latest') # Read only new incoming messages(ignore old messages)
      .option('failOnDataLoss', 'false') # if kafka deletes old messages(retention), spark wont crash
      .load() # start reading the kafka topic as a stream
      
      )

# Convert the 'value' column (Which is a json string) into structured columns
parsed_df = df.selectExpr("CAST(value AS STRING) as value") \
            .select(from_json(col("value"), kafka_data_schema).alias("data")) \
            .select("data.*")

processed_df = parsed_df.select(
       col("date").cast(TimestampType()).alias("date"),
       col("high").alias("high"),
       col("low").alias("low"),
       col("open").alias("open"),
       col("close").alias("close"),
       col("symbol").alias("symbol")
        
)

def write_to_postgres(batch_df, batch_id):
    """
    writes a microbatch DataFrame to postgreSQL using JDBC IN "append" mode.
    """
    batch_df.write \
    .format("jdbc") \
    .mode("append") \
    .options(**postgres_config) \
    .save()


# ---- Stream to PostgreSQL using foreachBatch

query = (
processed_df.writeStream 
.foreachBatch(write_to_postgres) #use foreachBatch for JDBC sinks
.option("checkpointLocation", checkpoint_dir) #directory where spark will store its
.outputMode('append') # or 'append', depending on your use case and table schema
.start()
)



#wait for the termination of the query (manually)
query.awaitTermination()


