# Table: fact_gl
**Type:** Fact | **Description:** General ledger journal entries.
## Columns
- gl_entry_id (INT): Unique entry key
- account_id (INT): Link to dim_account
- date_key (INT): Link to dim_date
- debit_amount (DECIMAL): Debit value
- credit_amount (DECIMAL): Credit value
- cost_center (VARCHAR): Cost center code
