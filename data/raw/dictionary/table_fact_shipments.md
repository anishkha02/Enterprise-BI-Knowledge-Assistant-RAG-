# Table: fact_shipments
**Type:** Fact | **Description:** One row per shipment.
## Columns
- shipment_id (INT): Unique shipment key
- order_id (INT): Link to fact_orders
- carrier (VARCHAR): Shipping carrier
- ship_date (DATE): Dispatch date
- delivery_date (DATE): Delivery date
- shipping_cost (DECIMAL): Cost of shipping
