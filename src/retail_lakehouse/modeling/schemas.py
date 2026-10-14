from pyspark.sql import types as T

CUSTOMER_SCHEMA = T.StructType(
    [
        T.StructField("customer_id", T.StringType(), True),
        T.StructField("first_name", T.StringType(), True),
        T.StructField("last_name", T.StringType(), True),
        T.StructField("email", T.StringType(), True),
        T.StructField("phone", T.StringType(), True),
        T.StructField("city", T.StringType(), True),
        T.StructField("country", T.StringType(), True),
        T.StructField("created_at", T.StringType(), True),
    ]
)

CATEGORIES_SCHEMA = T.StructType(
    [
        T.StructField("category_id", T.StringType(), True),
        T.StructField("category_name", T.StringType(), True),
        T.StructField("parent_category_id", T.StringType(), True),
    ]
)

PRODUCTS_SCHEMA = T.StructType(
    [
        T.StructField("product_id", T.StringType(), True),
        T.StructField("sku", T.StringType(), True),
        T.StructField("product_name", T.StringType(), True),
        T.StructField("category_id", T.StringType(), True),
        T.StructField("price", T.StringType(), True),
        T.StructField("cost", T.StringType(), True),
        T.StructField("is_active", T.StringType(), True),
        T.StructField("created_at", T.StringType(), True),
    ]
)

ORDERS_SCHEMA = T.StructType(
    [
        T.StructField("order_id", T.StringType(), True),
        T.StructField("customer_id", T.StringType(), True),
        T.StructField("order_status", T.StringType(), True),
        T.StructField("order_timestamp", T.StringType(), True),
        T.StructField("total_amount", T.StringType(), True),
        T.StructField("currency", T.StringType(), True),
        T.StructField("updated_at", T.StringType(), True),
    ]
)

ORDER_ITEMS_SCHEMA = T.StructType(
    [
        T.StructField("order_item_id", T.StringType(), True),
        T.StructField("order_id", T.StringType(), True),
        T.StructField("product_id", T.StringType(), True),
        T.StructField("quantity", T.StringType(), True),
        T.StructField("unit_price", T.StringType(), True),
        T.StructField("discount_amount", T.StringType(), True),
    ]
)

PAYMENTS_SCHEMA = T.StructType(
    [
        T.StructField("payment_id", T.StringType(), True),
        T.StructField("order_id", T.StringType(), True),
        T.StructField("payment_method", T.StringType(), True),
        T.StructField("payment_status", T.StringType(), True),
        T.StructField("amount", T.StringType(), True),
        T.StructField("payment_timestamp", T.StringType(), True),
        T.StructField("currency", T.StringType(), True),
    ]
)
