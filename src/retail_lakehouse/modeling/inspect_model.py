import logging

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from retail_lakehouse.config.logging import configure_logging
from retail_lakehouse.config.settings import settings
from retail_lakehouse.spark.session import create_spark_session

logger = logging.getLogger(__name__)


def load_customers(spark: SparkSession) -> DataFrame:
    return spark.read.csv(
        (settings.source_path / "customers" / "customers.csv").as_posix(),
        header=True,
        inferSchema=True,
    )


def load_products(spark: SparkSession) -> DataFrame:
    return spark.read.csv(
        (settings.source_path / "products" / "products.csv").as_posix(),
        header=True,
        inferSchema=True,
    )


def load_orders(spark: SparkSession) -> DataFrame:
    return spark.read.json(
        (settings.source_path / "orders" / "orders.jsonl").as_posix()
    )


def load_order_items(spark: SparkSession) -> DataFrame:
    return spark.read.csv(
        (settings.source_path / "order_items" / "order_items.csv").as_posix(),
        header=True,
        inferSchema=True,
    )


def inspect_primary_key(df: DataFrame, column: str):
    total = df.count()

    null_count = df.filter(F.col(column).isNull()).count()

    duplicate_count = total - df.select(column).distinct().count()

    print(f"\nColumn: {column}")
    print(f"Total rows: {total}")
    print(f"Null values: {null_count}")
    print(f"Duplicate rows by key: {duplicate_count}")


def inspect_composite_key(df: DataFrame, columns: list[str]):
    total = df.count()

    distinct_count = df.select(*columns).distinct().count()

    duplicate_count = total - distinct_count

    print(f"\nComposite key: {columns}")
    print(f"Total rows: {total}")
    print(f"Distinct combinations: {distinct_count}")
    print(f"Duplicate combinations: {duplicate_count}")


def inspect_model():
    configure_logging()

    spark = create_spark_session()

    try:
        customers = load_customers(spark)
        products = load_products(spark)
        orders = load_orders(spark)
        order_items = load_order_items(spark)

        print("\n========== CUSTOMER KEY ==========")
        inspect_primary_key(customers, "customer_id")

        print("\n========== PRODUCT KEY ==========")
        inspect_primary_key(products, "product_id")

        print("\n========== ORDER KEY ==========")
        inspect_primary_key(orders, "order_id")

        print("\n========== ORDER ITEM KEY ==========")
        inspect_primary_key(order_items, "order_item_id")
        inspect_composite_key(order_items, ["order_id", "product_id"])

        print("\n========== ORDER CUSTOMER REFERENCES ==========")
        invalid_customer_refs = orders.join(
            customers.select("customer_id"),
            on="customer_id",
            how="left_anti",
        )

        print("Invalid customer references:", invalid_customer_refs.count())
    finally:
        spark.stop()


if __name__ == "__main__":
    inspect_model()
