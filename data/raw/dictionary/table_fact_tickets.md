# Table: fact_tickets
**Type:** Fact | **Description:** Customer support tickets.
## Columns
- ticket_id (INT): Unique ticket key
- customer_id (INT): Link to dim_customer
- created_time (DATETIME): When the ticket was opened
- resolved_time (DATETIME): When the ticket was resolved
- priority (VARCHAR): Low, Medium or High
- status (VARCHAR): Open or Closed
