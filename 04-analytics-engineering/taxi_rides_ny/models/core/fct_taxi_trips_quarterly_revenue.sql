WITH Quarterly_Revenues AS (
    SELECT 
        DATE({{ dbt.date_trunc("year", "pickup_datetime") }}) AS revenue_year,  -- Convert to DATE
        CASE 
            WHEN EXTRACT(MONTH FROM pickup_datetime) IN (1,2,3) THEN 'Q1'
            WHEN EXTRACT(MONTH FROM pickup_datetime) IN (4,5,6) THEN 'Q2'
            WHEN EXTRACT(MONTH FROM pickup_datetime) IN (7,8,9) THEN 'Q3'
            WHEN EXTRACT(MONTH FROM pickup_datetime) IN (10,11,12) THEN 'Q4'
            ELSE NULL
        END AS revenue_quarter, 
        service_type, 
        SUM(total_amount) AS quarterly_revenue
    FROM {{ ref('fact_trips') }}
    GROUP BY 1,2,3
)

    SELECT 
        q1.revenue_year, 
        q1.revenue_quarter, 
        q1.service_type, 
        q1.quarterly_revenue, 
        q2.quarterly_revenue AS previous_year_quarterly_revenue,
        CASE 
            WHEN q2.quarterly_revenue IS NOT NULL 
            THEN (q1.quarterly_revenue / q2.quarterly_revenue) - 1
            ELSE NULL
        END AS quarterly_growth_rate
    FROM Quarterly_Revenues q1
    LEFT JOIN Quarterly_Revenues q2 
        ON q1.revenue_year = DATE_ADD(q2.revenue_year, INTERVAL 1 YEAR) 
        AND q1.revenue_quarter = q2.revenue_quarter
        AND q1.service_type = q2.service_type
