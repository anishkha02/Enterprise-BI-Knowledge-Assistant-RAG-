# KPI: Machine Downtime
**Domain:** Operations | **Owner:** Operations Analytics | **Refresh:** Monthly
**Definition:** Hours machines were not running when they were scheduled to.
**Formula:** SUM(scheduled_hours - run_hours)
**Source Tables:** fact_inventory
**Used In Reports:** Production Quality Dashboard (Power BI), Shipment Performance Report (SSRS)
**Notes:** Machine Downtime is part of the Operations KPI catalog.
