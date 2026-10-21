# Table: fact_payroll
**Type:** Fact | **Description:** Payroll records per pay period.
## Columns
- payroll_id (INT): Unique payroll key
- employee_id (INT): Link to dim_employee
- pay_period (VARCHAR): Pay period label
- gross_pay (DECIMAL): Gross pay amount
- overtime_hours (DECIMAL): Overtime hours worked
