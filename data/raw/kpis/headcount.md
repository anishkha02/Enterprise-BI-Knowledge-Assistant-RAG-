# KPI: Headcount
**Domain:** HR | **Owner:** HR Analytics | **Refresh:** Monthly
**Definition:** Total number of active employees at period end.
**Formula:** COUNT(employee_id) where status = Active
**Source Tables:** dim_employee, dim_department
**Used In Reports:** Workforce Analytics Dashboard (Power BI), Headcount and Attrition Report (SSRS)
**Notes:** Headcount is part of the HR KPI catalog.
