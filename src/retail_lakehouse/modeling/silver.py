from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def split_duplicate_keys(
    df: DataFrame, key_columns: list[str]
) -> tuple[DataFrame, DataFrame]:
    key_counts = (
        df.groupBy(*key_columns).count().withColumnRenamed("count", "_key_count")
    )
    joined = df.join(key_counts, on=key_columns, how="left")

    unique_rows = joined.filter(F.col("_key_count") == 1).drop("_key_count")
    duplicate_rows = joined.filter(F.col("_key_count") > 1).drop("_key_count")

    return unique_rows, duplicate_rows


def invalid_customers(df: DataFrame) -> DataFrame:
    return df.filter(
        F.col("customer_id").isNull()
        | (F.col("customer_id") == "")
        | F.col("created_att").isNull()
    )


def invalid_products(df: DataFrame) -> DataFrame:
    return df.filter(
        F.col("product_id").isNull()
        | (F.col("product_id") == "")
        | F.col("sku").isNull()
        | (F.col("sku") == "")
        | F.col("price").isNull()
        | (F.col("price") < 0)
        | F.col("cost").isNull()
        | (F.col("cost") < 0)
    )


def invalid_order_items(df: DataFrame) -> DataFrame:
    return df.filter(
        F.col("order_item_id").isNull()
        | (F.col("order_item_id") == "")
        | F.col("order_id").isNull()
        | F.col("product_id").isNull()
        | F.col("quantity").isNull()
        | (F.col("quantity") <= 0)
        | F.col("unit_price").isNull()
        | (F.col("unit_price") < 0)
        | F.col("discount_amount").isNull()
        | (F.col("discount_amount") < 0)
    )


def standardize_customers(df: DataFrame) -> DataFrame:
    return (
        df.select(
            F.trim("customer_id").alias("customer_id"),
            F.trim("first_name").alias("first_name"),
            F.trim("last_name").alias("last_name"),
            F.lower(F.trim("email")).alias("email"),
            F.trim("phone").alias("phone"),
            F.initcap(F.trim("city")).alias("city"),
            F.upper(F.trim("country")).alias("country"),
            F.to_timestamp("created_at").alias("created_at"),
        )
        .withColumn(
            "email",
            F.when(F.col("email") == "", F.lit(None).cast("string")).otherwise(
                F.col("email")
            ),
        )
        .withColumn(
            "city",
            F.when(F.col("city") == "", F.lit(None).cast("string")).otherwise(
                F.col("city")
            ),
        )
        .withColumn(
            "country",
            F.when(F.col("country") == "", F.lit(None).cast("string")).otherwise(
                F.col("country")
            ),
        )
    )


def standardize_products(df: DataFrame) -> DataFrame:
    return (
        df.select(
            F.trim("product_id").alias("product_id"),
            F.upper(F.trim("sku")).alias("sku"),
            F.trim("product_name").alias("product_name"),
            F.trim("category_id").alias("category_id"),
            F.expr("try_cast(price AS DECIMAL(18, 2))").alias("price"),
            F.expr("try_cast(cost AS DECIMAL(18, 2))").alias("cost"),
            F.lower(F.trim("is_active")).alias("is_active_raw"),
            F.to_timestamp("created_at").alias("created_at"),
        )
        .withColumn(
            "is_active",
            F.when(
                F.col("is_active_raw").isin("true", "1", "yes"),
                F.lit(True),
            )
            .when(
                F.col("is_active_raw").isin("false", "0", "no"),
                F.lit(False),
            )
            .otherwise(F.lit(None).cast("boolean")),
        )
        .drop("is_active_raw")
    )


def standardize_orders(df: DataFrame) -> DataFrame:
    return df.select(
        F.trim("order_id").alias("order_id"),
        F.trim("customer_id").alias("customer_id"),
        F.upper(F.trim("order_status")).alias("order_status"),
        F.to_timestamp("order_timestamp").alias("order_timestamp"),
        F.expr("try_cast(total_amount AS DECIMAL(18, 2))").alias("total_amount"),
        F.upper(F.trim("currency")).alias("currency"),
        F.to_timestamp("updated_at").alias("updated_at"),
    )


def standardize_order_items(df: DataFrame) -> DataFrame:
    return df.select(
        F.trim("order_item_id").alias("order_item_id"),
        F.trim("order_id").alias("order_id"),
        F.trim("product_id").alias("product_id"),
        F.expr("try_cast(quantity AS INT)").alias("quantity"),
        F.expr("try_cast(unit_price AS DECIMAL(18, 2))").alias("unit_price"),
        F.expr("try_cast(discount_amount AS DECIMAL(18, 2))").alias("discount_amount"),
    )


def standardize_categories(df: DataFrame) -> DataFrame:
    return df.select(
        F.trim("category_id").alias("category_id"),
        F.trim("category_name").alias("category_name"),
        F.trim("parent_category_id").alias("parent_category_id"),
    )


def standardize_payments(df: DataFrame) -> DataFrame:
    return df.select(
        F.trim("payment_id").alias("payment_id"),
        F.trim("order_id").alias("order_id"),
        F.upper(F.trim("payment_method")).alias("payment_method"),
        F.upper(F.trim("payment_status")).alias("payment_status"),
        F.expr("try_cast(amount AS DECIMAL(18, 2))").alias("amount"),
        F.to_timestamp("payment_timestamp").alias("payment_timestamp"),
        F.upper(F.trim("currency")).alias("currency"),
    )
