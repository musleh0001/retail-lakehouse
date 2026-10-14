from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def build_customer_dimension_initial(customers: DataFrame) -> DataFrame:
    window = Window.orderBy("customer_id")

    return (
        customers.withColumn(
            "customer_key",
            F.row_number().over(window).cast("long"),
        )
        .withColumn(
            "effective_from",
            F.to_date("created_at"),
        )
        .withColumn(
            "effective_to",
            F.lit("9999-12-31").cast("date"),
        )
        .withColumn("is_current", F.lit(True))
        .select(
            "customer_key",
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "country",
            "created_at",
            "effective_from",
            "effective_to",
            "is_current",
        )
    )


def build_product_dimension(products: DataFrame, categories: DataFrame) -> DataFrame:
    product_columns = products.alias("p")
    category_columns = categories.alias("c")

    joined = product_columns.join(
        category_columns,
        F.col("p.category_id") == F.col("c.category_id"),
        "left",
    )

    window = Window.orderBy(F.col("p.product_id"))

    return (
        joined.select(
            F.col("p.product_id"),
            F.col("p.sku"),
            F.col("p.product_name"),
            F.col("p.category_id"),
            F.col("c.category_name"),
            F.col("p.price"),
            F.col("p.cost"),
            F.col("p.is_active"),
            F.col("p.created_at"),
        )
        .withColumn(
            "product_key",
            F.row_number().over(window).cast("long"),
        )
        .select(
            "product_key",
            "product_id",
            "sku",
            "product_name",
            "category_id",
            "category_name",
            "price",
            "cost",
            "is_active",
            "created_at",
        )
    )


def build_date_dimension(spark, start_date: str, end_date: str) -> DataFrame:
    return (
        spark.range(1)
        .select(
            F.explode(
                F.sequence(
                    F.to_date(F.lit(start_date)),
                    F.to_date(F.lit(end_date)),
                    F.expr("INTERVAL 1 DAY"),
                )
            ).alias("date")
        )
        .withColumn(
            "date_key",
            F.date_format("date", "yyyyMMdd").cast("int"),
        )
        .withColumn("year", F.year("date"))
        .withColumn("quarter", F.quarter("date"))
        .withColumn("month", F.month("date"))
        .withColumn("month_name", F.date_format("date", "MMMM"))
        .withColumn("day_of_month", F.dayofmonth("date"))
        .withColumn("day_of_week", F.dayofweek("date"))
        .withColumn("day_name", F.date_format("date", "EEEE"))
        .withColumn(
            "is_weekend",
            F.dayofweek("date").isin(1, 7),
        )
        .select(
            "date_key",
            "date",
            "year",
            "quarter",
            "month",
            "month_name",
            "day_of_month",
            "day_of_week",
            "day_name",
            "is_weekend",
        )
    )
