from dataclasses import dataclass


@dataclass(frozen=True)
class DimensionDefinition:
    name: str
    grain: str
    surrogate_key: str
    business_key: str


@dataclass(frozen=True)
class FactDefinition:
    name: str
    grain: str
    measures: tuple[str, ...]
    foreign_keys: tuple[str, ...]


DIM_CUSTOMER = DimensionDefinition(
    name="dim_customer",
    grain="One row represents one customer dimension record",
    surrogate_key="customer_key",
    business_key="customer_id",
)

DIM_PRODUCT = DimensionDefinition(
    name="dim_product",
    grain="One row represents one product dimension record",
    surrogate_key="product_key",
    business_key="product_id",
)

DIM_DATE = DimensionDefinition(
    name="dim_date",
    grain="One row represents one calendar date",
    surrogate_key="date_key",
    business_key="full_date",
)

FACT_ORDER_ITEM = FactDefinition(
    name="fact_order_item",
    grain="One row represents one product line within one order",
    measures=(
        "quantity",
        "unit_price",
        "discount_amount",
        "gross_amount",
        "net_amount",
    ),
    foreign_keys=(
        "customer_key",
        "product_key",
        "date_key",
    ),
)
