# Table: fact_orders
**Type:** Fact | **Description:** One row per customer order.
## Columns
- order_id (INT): Unique order key
- customer_id (INT): Link to dim_customer
- order_date (DATE): Date the order was placed
- ship_date (DATE): Date the order was shipped
- order_amount (DECIMAL): Total order value
- status (VARCHAR): Open, Shipped or Cancelled
