# Table: fact_recruitment
**Type:** Fact | **Description:** Job requisitions and hiring outcomes.
## Columns
- requisition_id (INT): Unique requisition key
- department_id (INT): Link to dim_department
- posting_date (DATE): Job posting date
- offer_accepted_date (DATE): Date offer accepted
- recruiting_cost (DECIMAL): Cost of recruiting
