# KPI: Active Customers
**Domain:** Customer | **Owner:** Customer Analytics | **Refresh:** Monthly
**Definition:** Customers with at least one order in the last 90 days.
**Formula:** COUNT(DISTINCT customer_id) with an order in last 90 days
**Source Tables:** dim_customer, fact_orders
**Used In Reports:** Support Operations Dashboard (Power BI), Support Ticket Summary (SSRS)
**Notes:** Active Customers is part of the Customer KPI catalog.
