import csv
import json
import logging
from pathlib import Path

from retail_lakehouse.config.logging import configure_logging
from retail_lakehouse.config.settings import settings

logger = logging.getLogger(__name__)


def inspect_csv(path: Path):
    logger.info("Inspecting CSV: %s", path)

    with path.open(
        mode="r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        records = list(reader)

    logger.info("Columns: %s", reader.fieldnames)
    logger.info("Total records: %s", len(records))

    for record in records[:3]:
        print(record)


def inspect_jsonl(path: Path):
    logger.info("Inspecting JSONL: %s", path)

    records = []

    with path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    logger.info("Total records: %s", len(records))

    if records:
        logger.info("Columns: %s", list(records[0].keys()))

    for record in records[:3]:
        print(record)


def main():
    configure_logging()

    source = settings.source_path

    csv_files = [
        source / "customers" / "customers.csv",
        source / "products" / "products.csv",
        source / "categories" / "categories.csv",
        source / "order_items" / "order_items.csv",
    ]

    jsonl_files = [
        source / "orders" / "orders.jsonl",
        source / "payments" / "payments.jsonl",
    ]

    for path in csv_files:
        if path.exists():
            inspect_csv(path)

    for path in jsonl_files:
        if path.exists():
            inspect_jsonl(path)


if __name__ == "__main__":
    main()
