# 1. Configure Application Logging
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting ShopSphere Bare-Metal Batch ETL Pipeline...")

# 2. Initialize SparkSession
spark = SparkSession.builder.appName("ShopSphere-ETL").getOrCreate()
logger.info("Spark Session created successfully.")

# 3. Extract Raw Data from HDFS Bronze Zone
raw_path = "hdfs://localhost:9000/capstone_project/raw_data/ecommerce_logs"
logger.info(f"Extracting raw data from HDFS path: {raw_path}")
df_raw = spark.read.csv(raw_path, header=True, inferSchema=True)

# 4. Transform & Cleanse Data
logger.info("Applying schema validation, null filtering, and date extraction...")
df_clean = df_raw.dropna(subset=["event_time", "event_type", "product_id"]) \
                 .filter(col("price") > 0) \
                 .withColumn("event_date", to_date(col("event_time")))

# 5. Load Optimized Data to Processed Zone
processed_path = "hdfs://localhost:9000/capstone_project/processed_data/ecommerce_parquet"
logger.info(f"Writing partitioned Parquet files to HDFS path: {processed_path}")
df_clean.write.mode("overwrite").partitionBy("event_date").parquet(processed_path)

logger.info("Pipeline executed successfully. Stopping SparkSession...")
spark.stop()
