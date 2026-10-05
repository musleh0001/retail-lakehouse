import logging

from pyspark.sql import SparkSession

from retail_lakehouse.config.logging import configure_logging
from retail_lakehouse.config.settings import settings
from retail_lakehouse.spark.session import create_spark_session

logger = logging.getLogger(__name__)


def main():
    configure_logging()

    spark = create_spark_session()

    try:
        customers_df = spark.read.csv(
            (settings.source_path / "customers" / "customers.csv").as_posix(),
            header=True,
            inferSchema=True,
        )
        orders_df = spark.read.json(
            (settings.source_path / "orders" / "orders.jsonl").as_posix()
        )

        print("\n=== CUSTOMERS ===")
        customers_df.printSchema()
        customers_df.show(5, truncate=False)

        print("\n=== ORDERS ===")
        orders_df.printSchema()
        orders_df.show(5, truncate=False)

        print("\n=== DATASET COUNTS ===")
        print("Customers: ", customers_df.count())
        print("Orders: ", orders_df.count())

        print("\n=== DATASET COUNTS ===")
        print(spark.version)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
