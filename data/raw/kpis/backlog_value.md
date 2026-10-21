# KPI: Backlog Value
**Domain:** Sales | **Owner:** Sales Analytics | **Refresh:** Monthly
**Definition:** Value of confirmed orders not yet delivered.
**Formula:** SUM(order_amount) where status = Open
**Source Tables:** fact_orders
**Used In Reports:** Sales Pipeline Dashboard (Power BI), Regional Sales Detail (SSRS)
**Notes:** Backlog Value is part of the Sales KPI catalog.
