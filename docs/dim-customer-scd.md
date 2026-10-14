# Customer Dimension — SCD Type 2

## Grain

One row represents one historical version of one customer.

## Business Key

`customer_id`

## Surrogate Key

`customer_key`

## Type 2 Attributes

- city
- country

## Type 1 Attributes

- email
- phone

## Type 0 Attributes

- customer_id
- created_at

## Historical Columns

- effective_from
- effective_to
- is_current