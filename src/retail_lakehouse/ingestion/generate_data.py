import csv
import json
import logging
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from retail_lakehouse.config.logging import configure_logging
from retail_lakehouse.config.settings import settings

logger = logging.getLogger(__name__)


FIRST_NAMES = [
    "John",
    "Jane",
    "Michael",
    "Sarah",
    "David",
    "Emma",
    "James",
    "Olivia",
    "Robert",
    "Sophia",
    "Daniel",
    "Emily",
    "Mohammed",
    "Ayesha",
    "Rahim",
    "Nusrat",
    "Tanvir",
    "Fatima",
    "Arif",
    "Sadia",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Brown",
    "Taylor",
    "Wilson",
    "Anderson",
    "Thomas",
    "Jackson",
    "White",
    "Harris",
    "Khan",
    "Rahman",
    "Ahmed",
    "Chowdhury",
    "Hasan",
    "Islam",
    "Hossain",
    "Akter",
]

CITIES = [
    "Dhaka",
    "Chittagong",
    "Sylhet",
    "Khulna",
    "London",
    "New York",
    "Singapore",
    "Toronto",
    "Dubai",
    "Kolkata",
]

COUNTRIES = {
    "Dhaka": "Bangladesh",
    "Chittagong": "Bangladesh",
    "Sylhet": "Bangladesh",
    "Khulna": "Bangladesh",
    "London": "United Kingdom",
    "New York": "United States",
    "Singapore": "Singapore",
    "Toronto": "Canada",
    "Dubai": "United Arab Emirates",
    "Kolkata": "India",
}

CATEGORY_NAMES = [
    "Electronics",
    "Computers",
    "Mobile Phones",
    "Fashion",
    "Men Clothing",
    "Women Clothing",
    "Home & Kitchen",
    "Furniture",
    "Books",
    "Sports",
    "Beauty",
    "Accessories",
]

PRODUCT_NAMES = [
    "Wireless Headphones",
    "Bluetooth Speaker",
    "Smart Watch",
    "Gaming Mouse",
    "Mechanical Keyboard",
    "Laptop Stand",
    "USB-C Hub",
    "Running Shoes",
    "Cotton T-Shirt",
    "Leather Wallet",
    "Office Chair",
    "Coffee Maker",
    "Water Bottle",
    "Backpack",
    "Smartphone Case",
    "Desk Lamp",
    "Fitness Tracker",
    "External SSD",
    "Travel Bag",
    "Sunglasses",
]

ORDER_STATUSES = [
    "pending",
    "confirmed",
    "processing",
    "shipped",
    "delivered",
    "cancelled",
    "returned",
]

PAYMENT_METHODS = [
    "credit_card",
    "debit_card",
    "mobile_banking",
    "bank_transfer",
    "cash_on_delivery",
]

PAYMENT_STATUSES = [
    "pending",
    "successful",
    "failed",
    "refunded",
]


BASE_DATE = datetime(
    2025,
    1,
    1,
    tzinfo=timezone.utc,
)


def random_datetime(
    rng: random.Random,
    start: datetime = BASE_DATE,
    end: datetime | None = None,
) -> datetime:
    """Generate a random UTC datetime."""

    if end is None:
        end = datetime.now(timezone.utc)

    total_seconds = int((end - start).total_seconds())

    return start + timedelta(seconds=rng.randint(0, max(total_seconds, 0)))


def iso_timestamp(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def random_money(
    rng: random.Random,
    minimum: Decimal,
    maximum: Decimal,
) -> str:
    """Generate a monetary amount with two decimal places."""

    amount = rng.uniform(float(minimum), float(maximum))

    return str(Decimal(str(amount)).quantize(Decimal("0.01")))


def write_csv(
    path: Path,
    records: list[dict],
) -> None:
    """Write records into a CSV file."""

    if not records:
        logger.warning("No records to write: %s", path)
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(records[0].keys()),
        )

        writer.writeheader()
        writer.writerows(records)

    logger.info(
        "Generated CSV: %s | records=%s",
        path,
        len(records),
    )


def write_jsonl(
    path: Path,
    records: list[dict],
) -> None:
    """Write one JSON object per line."""

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    logger.info(
        "Generated JSONL: %s | records=%s",
        path,
        len(records),
    )


def generate_categories(
    rng: random.Random,
) -> list[dict]:

    records = []

    for index, category_name in enumerate(
        CATEGORY_NAMES,
        start=1,
    ):
        parent_id = None

        if index in (2, 3, 5, 6, 8):
            parent_id = f"CAT-{index - 1:03d}"

        records.append(
            {
                "category_id": f"CAT-{index:03d}",
                "category_name": category_name,
                "parent_category_id": parent_id or "",
            }
        )

    return records


def generate_customers(
    rng: random.Random,
    count: int,
) -> list[dict]:

    records = []

    for index in range(1, count + 1):
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)

        city = rng.choice(CITIES)

        created_at = random_datetime(rng)

        email = f"{first_name.lower()}.{last_name.lower()}{index}@example.com"

        phone = (
            f"+8801{rng.randint(300000000, 999999999)}"
            if city in CITIES[:4]
            else f"+1{rng.randint(2000000000, 9999999999)}"
        )

        records.append(
            {
                "customer_id": f"CUST-{index:06d}",
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "city": city,
                "country": COUNTRIES[city],
                "created_at": iso_timestamp(created_at),
            }
        )

    # Deliberately introduce data-quality issues.

    for record in records[:10]:
        record["email"] = ""

    for record in records[10:20]:
        record["city"] = record["city"].upper()

    for record in records[20:30]:
        record["phone"] = "INVALID_PHONE"

    # Introduce duplicate customer records.
    if len(records) >= 2:
        duplicate = records[0].copy()
        duplicate["first_name"] = "Modified"
        records.append(duplicate)

    return records


def generate_products(
    rng: random.Random,
    categories: list[dict],
    count: int,
) -> list[dict]:

    records = []

    category_ids = [category["category_id"] for category in categories]

    for index in range(1, count + 1):
        product_name = rng.choice(PRODUCT_NAMES)

        price = random_money(
            rng,
            Decimal("10.00"),
            Decimal("1500.00"),
        )

        cost = str(
            (Decimal(price) * Decimal(str(rng.uniform(0.35, 0.85)))).quantize(
                Decimal("0.01")
            )
        )

        created_at = random_datetime(rng)

        records.append(
            {
                "product_id": f"PROD-{index:06d}",
                "sku": f"SKU-{index:06d}",
                "product_name": product_name,
                "category_id": rng.choice(category_ids),
                "price": price,
                "cost": cost,
                "is_active": rng.choice(["true", "false"]),
                "created_at": iso_timestamp(created_at),
            }
        )

    # Introduce missing category reference.
    if records:
        records[0]["category_id"] = "CAT-999"

    # Introduce a missing product price.
    if len(records) > 1:
        records[1]["price"] = ""

    return records


def generate_orders(
    rng: random.Random,
    customers: list[dict],
    count: int,
) -> list[dict]:

    records = []

    valid_customer_ids = [
        customer["customer_id"] for customer in customers if customer["customer_id"]
    ]

    for index in range(1, count + 1):
        customer_id = rng.choice(valid_customer_ids)

        order_timestamp = random_datetime(rng)

        total_amount = random_money(
            rng,
            Decimal("20.00"),
            Decimal("5000.00"),
        )

        records.append(
            {
                "order_id": f"ORD-{index:08d}",
                "customer_id": customer_id,
                "order_status": rng.choice(ORDER_STATUSES),
                "order_timestamp": iso_timestamp(order_timestamp),
                "total_amount": total_amount,
                "currency": "USD",
                "updated_at": iso_timestamp(
                    order_timestamp + timedelta(hours=rng.randint(0, 72))
                ),
            }
        )

    # Introduce invalid customer reference.
    if records:
        records[0]["customer_id"] = "CUST-999999"

    # Introduce inconsistent status.
    if len(records) > 1:
        records[1]["order_status"] = "DELIVERED"

    # Introduce duplicate order.
    if len(records) > 2:
        duplicate = records[2].copy()
        duplicate["total_amount"] = "9999.99"
        records.append(duplicate)

    # Introduce malformed monetary value.
    if len(records) > 3:
        records[3]["total_amount"] = "INVALID_AMOUNT"

    # Introduce missing timestamp.
    if len(records) > 4:
        records[4]["order_timestamp"] = ""

    return records


def generate_order_items(
    rng: random.Random,
    orders: list[dict],
    products: list[dict],
) -> list[dict]:

    records = []

    product_ids = [product["product_id"] for product in products]

    item_counter = 1

    for order in orders:
        # A duplicated source order may generate duplicate items.
        item_count = rng.randint(1, 5)

        for _ in range(item_count):
            quantity = rng.randint(1, 5)

            unit_price = random_money(
                rng,
                Decimal("10.00"),
                Decimal("1500.00"),
            )

            discount = random_money(
                rng,
                Decimal("0.00"),
                Decimal("100.00"),
            )

            records.append(
                {
                    "order_item_id": f"ITEM-{item_counter:010d}",
                    "order_id": order["order_id"],
                    "product_id": rng.choice(product_ids),
                    "quantity": str(quantity),
                    "unit_price": unit_price,
                    "discount_amount": discount,
                }
            )

            item_counter += 1

    # Introduce invalid product reference.
    if records:
        records[0]["product_id"] = "PROD-999999"

    # Introduce invalid quantity.
    if len(records) > 1:
        records[1]["quantity"] = "-5"

    # Introduce a duplicate order item.
    if len(records) > 2:
        duplicate = records[2].copy()
        records.append(duplicate)

    return records


def generate_payments(
    rng: random.Random,
    orders: list[dict],
) -> list[dict]:

    records = []

    payment_counter = 1

    # Use original order identifiers, excluding duplicate order rows.
    seen_orders = set()

    for order in orders:
        order_id = order["order_id"]

        if order_id in seen_orders:
            continue

        seen_orders.add(order_id)

        payment_count = rng.choices(
            population=[1, 2],
            weights=[0.85, 0.15],
            k=1,
        )[0]

        for _ in range(payment_count):
            payment_timestamp = random_datetime(rng)

            records.append(
                {
                    "payment_id": f"PAY-{payment_counter:010d}",
                    "order_id": order_id,
                    "payment_method": rng.choice(PAYMENT_METHODS),
                    "payment_status": rng.choice(PAYMENT_STATUSES),
                    "amount": order["total_amount"],
                    "payment_timestamp": iso_timestamp(payment_timestamp),
                    "currency": order["currency"],
                }
            )

            payment_counter += 1

    # Introduce invalid order reference.
    if records:
        records[0]["order_id"] = "ORD-99999999"

    # Introduce malformed amount.
    if len(records) > 1:
        records[1]["amount"] = "UNKNOWN"

    return records


def generate_dataset() -> None:

    configure_logging()

    rng = random.Random(settings.generator_seed)

    logger.info("Starting retail dataset generation")
    logger.info("Random seed: %s", settings.generator_seed)

    settings.create_directories()

    categories = generate_categories(rng)

    customers = generate_customers(
        rng,
        settings.customer_count,
    )

    products = generate_products(
        rng,
        categories,
        settings.product_count,
    )

    orders = generate_orders(
        rng,
        customers,
        settings.order_count,
    )

    order_items = generate_order_items(
        rng,
        orders,
        products,
    )

    payments = generate_payments(
        rng,
        orders,
    )

    source = settings.source_path

    write_csv(
        source / "categories" / "categories.csv",
        categories,
    )

    write_csv(
        source / "customers" / "customers.csv",
        customers,
    )

    write_csv(
        source / "products" / "products.csv",
        products,
    )

    write_jsonl(
        source / "orders" / "orders.jsonl",
        orders,
    )

    write_csv(
        source / "order_items" / "order_items.csv",
        order_items,
    )

    write_jsonl(
        source / "payments" / "payments.jsonl",
        payments,
    )

    logger.info("Dataset generation completed")

    logger.info("Generated dataset summary:")
    logger.info("Categories: %s", len(categories))
    logger.info("Customers: %s", len(customers))
    logger.info("Products: %s", len(products))
    logger.info("Orders: %s", len(orders))
    logger.info("Order items: %s", len(order_items))
    logger.info("Payments: %s", len(payments))
