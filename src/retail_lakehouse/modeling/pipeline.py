import logging

from pyspark.sql import functions as F

from retail_lakehouse.modeling.dimensions import (
    build_customer_dimension_initial,
    build_date_dimension,
    build_product_dimension,
)
from retail_lakehouse.modeling.facts import build_order_item_fact
from retail_lakehouse.modeling.silver import (
    invalid_customers,
    invalid_products,
    split_duplicate_keys,
    standardize_categories,
    standardize_customers,
    standardize_order_items,
    standardize_orders,
    standardize_payments,
    standardize_products,
)
from retail_lakehouse.modeling.source_reader import read_bronze
from retail_lakehouse.spark.session import create_spark_session

logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    spark = create_spark_session()

    try:
        # 1. Read source files
        bronze = read_bronze(spark)

        # 2. Standardize source values
        customers = standardize_customers(bronze["customers"])
        products = standardize_products(bronze["products"])
        categories = standardize_categories(bronze["categories"])
        orders = standardize_orders(bronze["orders"])
        order_items = standardize_order_items(bronze["order_items"])
        payments = standardize_payments(bronze["payments"])

        # 3. Identify duplicate customer business keys
        unique_customers, duplicate_customers = split_duplicate_keys(
            customers.filter("customer_id IS NOT NULL"),
            ["customer_id"],
        )

        logger.info("Customer rows with duplicate business keys identified")
        duplicate_customers.show(10, truncate=False)

        # This initial pipeline proceeds only with unique customer IDs.
        # Conflicting duplicates need an explicit resolution policy.
        customers = unique_customers

        # 4. Apply initial customer/product validity rules
        bad_customers = invalid_customers(customers)
        bad_products = invalid_products(products)

        logger.info("Invalid customer rows")
        bad_customers.show(10, truncate=False)

        logger.info("Invalid product rows")
        bad_products.show(10, truncate=False)

        customers = customers.join(
            bad_customers.select("customer_id").distinct(),
            on="customer_id",
            how="left_anti",
        )

        products = products.join(
            bad_products.select("product_id").distinct(),
            on="product_id",
            how="left_anti",
        )

        # 5. Build dimensions
        dim_customer = build_customer_dimension_initial(customers)

        dim_product = build_product_dimension(
            products,
            categories,
        )

        order_dates = orders.select(F.to_date("order_timestamp").alias("date"))

        bounds = order_dates.agg(
            F.min("date").alias("min_date"),
            F.max("date").alias("max_date"),
        ).first()

        if bounds["min_date"] is None:  # type: ignore
            raise ValueError("No valid order dates found")

        dim_date = build_date_dimension(
            spark,
            str(bounds["min_date"]),
            str(bounds["max_date"]),  # type: ignore
        )

        # 6. Build the transaction fact
        fact = build_order_item_fact(
            order_items,
            orders,
            dim_customer,
            dim_product,
            dim_date,
        )

        # 7. Inspect the output
        for name, df in {
            "dim_customer": dim_customer,
            "dim_product": dim_product,
            "dim_date": dim_date,
            "fact_order_item": fact,
        }.items():
            logger.info("Output: %s", name)
            df.printSchema()
            df.show(10, truncate=False)

    finally:
        spark.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline()
