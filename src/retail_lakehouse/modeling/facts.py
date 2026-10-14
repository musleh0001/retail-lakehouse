from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_order_item_fact(
    order_items: DataFrame,
    orders: DataFrame,
    customer_dimension: DataFrame,
    product_dimension: DataFrame,
    date_dimension: DataFrame,
) -> DataFrame:
    oi = order_items.alias("oi")
    o = orders.alias("o")

    # Keep only the current customer version for this initial-load
    # pipeline. Historical event-date resolution is covered below.
    customers = customer_dimension.alias("c")
    products = product_dimension.alias("p")
    dates = date_dimension.alias("d")

    joined = (
        oi.join(o, F.col("oi.order_id") == F.col("o.order_id"), "inner")
        .join(
            customers,
            F.col("o.customer_id") == F.col("c.customer_id"),
            "left",
        )
        .join(
            products,
            F.col("oi.product_id") == F.col("p.product_id"),
            "left",
        )
        .join(
            dates,
            F.to_date(F.col("o.order_timestamp")) == F.col("d.date"),
            "left",
        )
    )

    gross = F.col("oi.quantity").cast("decimal(18, 2)") * F.col("oi.unit_price")

    return joined.select(
        F.col("oi.order_item_id").alias("order_item_id"),
        F.col("oi.order_id").alias("order_id"),
        F.col("c.customer_key").alias("customer_key"),
        F.col("p.product_key").alias("product_key"),
        F.col("d.date_key").alias("date_key"),
        F.col("oi.quantity").alias("quantity"),
        F.col("oi.unit_price").alias("unit_price"),
        F.col("oi.discount_amount").alias("discount_amount"),
        gross.alias("gross_amount"),
        (gross - F.col("oi.discount_amount")).alias("net_amount"),
        F.col("o.currency").alias("currency"),
        F.col("o.order_status").alias("order_status"),
    )
