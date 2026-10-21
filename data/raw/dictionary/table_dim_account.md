# Table: dim_account
**Type:** Dimension | **Description:** Chart of accounts for the general ledger.
## Columns
- account_id (INT): Unique account key
- account_name (VARCHAR): Account name
- account_type (VARCHAR): Asset, Liability, Revenue or Expense
- parent_account_id (INT): Parent account for roll-ups
