# Table: fact_sales
**Type:** Fact | **Description:** One row per order line sold.
## Columns
- sale_id (INT): Unique sale line key
- order_id (INT): Link to fact_orders
- product_id (INT): Link to dim_product
- date_key (INT): Link to dim_date
- quantity (INT): Units sold
- sales_amount (DECIMAL): Revenue for the line
- discount_amount (DECIMAL): Discount given
