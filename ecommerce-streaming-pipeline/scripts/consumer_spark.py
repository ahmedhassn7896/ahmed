import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Required packages for Pyspark with Kafka and PostgreSQL
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.6.0 pyspark-shell'

def write_to_postgres(df, epoch_id):
    """Sinks a micro-batch into PostgreSQL."""
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/ecommerce_db") \
        .option("dbtable", "transactions") \
        .option("user", "ecommerce_user") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

def main():
    spark = SparkSession.builder \
        .appName("EcommerceRealTimeAnalytics") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    # Define schema matching data_generator
    schema = StructType([
        StructField("transaction_id", StringType()),
        StructField("user_id", StringType()),
        StructField("product_id", StringType()),
        StructField("amount", DoubleType()),
        StructField("status", StringType()),
        StructField("transaction_time", TimestampType())
    ])

    # Read stream from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "ecommerce_transactions") \
        .option("startingOffsets", "latest") \
        .load()

    # Parse JSON
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Write stream to PostgreSQL via foreachBatch
    query = parsed_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
