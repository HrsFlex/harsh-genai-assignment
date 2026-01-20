from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, round, hour, dayofmonth, from_unixtime

def create_spark_session(app_name="MobilityAnalyticsETL"):
    """
    Creates and returns a SparkSession.
    """
    return SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()

def process_data(input_path, output_path):
    """
    Reads, cleans, and computes KPIs using PySpark.
    """
    spark = create_spark_session()
    

    print(f"Reading data from {input_path}...")
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)
    
    initial_count = df.count()
    print(f"Initial Count: {initial_count}")
    

    df_clean = df.filter(
        (col("passenger_count") > 0) & 
        (col("trip_distance") > 0) & 
        (col("total_amount") > 0)
    )
    

    df_clean = df_clean.filter(
        (col("pickup_latitude").between(40.5, 40.95)) &
        (col("pickup_longitude").between(-74.25, -73.7))
    )
    

    df_clean = df_clean.withColumn("pickup_time", col("tpep_pickup_datetime").cast("timestamp")) \
                       .withColumn("dropoff_time", col("tpep_dropoff_datetime").cast("timestamp"))
    

    df_clean = df_clean.withColumn("pickup_hour", hour(col("pickup_time"))) \
                       .withColumn("pickup_day", dayofmonth(col("pickup_time")))
    

    df_clean = df_clean.withColumn("trip_duration_min", 
        (unix_timestamp(col("dropoff_time")) - unix_timestamp(col("pickup_time"))) / 60
    )
    

    

    revenue_daily = df_clean.groupBy("pickup_day") \
        .agg({"total_amount": "sum", "fare_amount": "avg"}) \
        .orderBy("pickup_day")
        

    hourly_demand = df_clean.groupBy("pickup_hour") \
        .count() \
        .orderBy("pickup_hour")
        

    print(f"Writing results to {output_path}...")
    

    df_clean.write.mode("overwrite").partitionBy("pickup_day").parquet(f"{output_path}/cleaned_trips")
    

    revenue_daily.write.mode("overwrite").csv(f"{output_path}/revenue_daily")
    hourly_demand.write.mode("overwrite").csv(f"{output_path}/hourly_demand")
    
    spark.stop()
    print("ETL Job Complete.")

if __name__ == "__main__":

    INPUT_FILE = "c:/Users/HarshKumar/OneDrive - Blend 360/Projects/dataset/yellow_tripdata_2016-01.csv"
    OUTPUT_DIR = "c:/Users/HarshKumar/OneDrive - Blend 360/Projects/spark_output"
    
    try:
        process_data(INPUT_FILE, OUTPUT_DIR)
    except Exception as e:
        print(f"Spark execution failed (ensure Java/Hadoop is set up): {e}")
