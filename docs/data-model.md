<div align="center">
    <h1>Retail Lakehouse Data Model</h1>
</div>

## Customer

### Grain

One row represents one customer.

### Primary Key

`customer_id`

### Relationships

One customer can place many orders.

---

## Category

### Grain

One row represents one product category.

### Primary Key

`category_id`

### Relationships

One category can contain many products.

A category may optionally have a parent category.

---

## Product

### Grain

One row represents one product.

### Primary Key

`product_id`

### Relationships

One product belongs to one category.

One product can appear in many order items.

---

## Order

### Grain

One row represents one customer order.

### Primary Key

`order_id`

### Relationships

One order belongs to one customer.

One order can contain many order items.

One order can have multiple payment transactions.

---

## Order Item

### Grain

One row represents one product line within one order.

### Primary Key

`order_item_id`

### Relationships

One order item belongs to one order.

One order item references one product.

---

## Payment

### Grain

One row represents one payment transaction.

### Primary Key

`payment_id`

### Relationships

One payment belongs to one order.

# Relational Model

## Customer

### Grain
One row represents one customer.

### Primary Key
`customer_id`

### Candidate Keys
- `customer_id`
- `email` when populated and unique

### Attributes

| Column | Meaning |
|---|---|
| customer_id | Internal customer identifier |
| first_name | Customer first name |
| last_name | Customer last name |
| email | Customer email |
| phone | Customer phone |
| city | Customer city |
| country | Customer country |
| created_at | Customer creation timestamp |


# Relationships

## Customer → Order

Cardinality:

`1:N`

A customer can place many orders.

Foreign key:

`orders.customer_id → customers.customer_id`

---

## Order → Order Item

Cardinality:

`1:N`

An order can contain multiple order items.

Foreign key:

`order_items.order_id → orders.order_id`

---

## Product → Order Item

Cardinality:

`1:N`

A product can appear in many order items.

Foreign key:

`order_items.product_id → products.product_id`

---

## Category → Product

Cardinality:

`1:N`

A category can contain many products.

Foreign key:

`products.category_id → categories.category_id`

---

## Order → Payment

Cardinality:

`1:N`

An order can have multiple payment transactions.

Foreign key:

`payments.order_id → orders.order_id`