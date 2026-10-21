# KPI: New Customers
**Domain:** Customer | **Owner:** Customer Analytics | **Refresh:** Monthly
**Definition:** Customers who placed their first order in the period.
**Formula:** COUNT(customer_id) where first_order_date is in period
**Source Tables:** dim_customer, fact_orders
**Used In Reports:** Customer Health Dashboard (Power BI), Monthly Retention Report (SSRS)
**Notes:** New Customers is part of the Customer KPI catalog.
