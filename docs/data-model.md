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