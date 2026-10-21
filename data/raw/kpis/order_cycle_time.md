# KPI: Order Cycle Time
**Domain:** Operations | **Owner:** Operations Analytics | **Refresh:** Monthly
**Definition:** Average time from order placement to shipment.
**Formula:** AVG(ship_date - order_date)
**Source Tables:** fact_orders, fact_shipments
**Used In Reports:** Supply Chain Dashboard (Power BI), Inventory Status Report (SSRS)
**Notes:** Order Cycle Time is part of the Operations KPI catalog.
