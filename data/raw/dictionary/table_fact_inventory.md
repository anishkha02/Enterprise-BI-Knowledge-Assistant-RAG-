# Table: fact_inventory
**Type:** Fact | **Description:** Daily inventory and production snapshot.
## Columns
- inventory_id (INT): Unique snapshot key
- product_id (INT): Link to dim_product
- warehouse (VARCHAR): Warehouse name
- date_key (INT): Link to dim_date
- quantity_on_hand (INT): Units in stock
- reorder_point (INT): Stock level that triggers reorder
