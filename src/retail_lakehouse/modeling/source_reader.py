from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import types as T

from retail_lakehouse.config.settings import settings
from retail_lakehouse.modeling.schemas import (
    CATEGORIES_SCHEMA,
    CUSTOMER_SCHEMA,
    ORDER_ITEMS_SCHEMA,
    ORDERS_SCHEMA,
    PAYMENTS_SCHEMA,
    PRODUCTS_SCHEMA,
)

FileFormat = Literal["csv", "jsonl"]


@dataclass(frozen=True)
class DatasetSource:
    filename: str
    format: FileFormat
    schema: T.StructType
    header: bool = True


# Declarative registry: Easy to maintain, test, and extend
DATASET_REGISTRY: dict[str, DatasetSource] = {
    "customers": DatasetSource("customers/customers.csv", "csv", CUSTOMER_SCHEMA),
    "categories": DatasetSource("categories/categories.csv", "csv", CATEGORIES_SCHEMA),
    "products": DatasetSource("products/products.csv", "csv", PRODUCTS_SCHEMA),
    "orders": DatasetSource("orders/orders.jsonl", "jsonl", ORDERS_SCHEMA),
    "order_items": DatasetSource(
        "order_items/order_items.csv", "csv", ORDER_ITEMS_SCHEMA
    ),
    "payments": DatasetSource("payments/payments.jsonl", "jsonl", PAYMENTS_SCHEMA),
}


def read_dataset(
    spark: SparkSession, base_path: Path, source: DatasetSource
) -> DataFrame:
    path = (base_path / source.filename).as_posix()
    reader = spark.read.schema(source.schema)

    match source:
        case DatasetSource(format="csv", header=True):
            return reader.csv(path, header=True)
        case DatasetSource(format="csv", header=False):
            return reader.csv(path, header=False)
        case DatasetSource(format="jsonl"):
            return reader.json(path)
        case _:
            raise ValueError(f"Unsupported format")


def read_bronze(spark: SparkSession) -> dict[str, DataFrame]:
    return {
        name: read_dataset(spark, settings.source_path, DATASET_REGISTRY[name])
        for name in DATASET_REGISTRY.keys()
    }
