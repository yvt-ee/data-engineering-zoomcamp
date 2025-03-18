{{ config(materialized='table') }}

WITH trip_duration AS (
    SELECT
        PUlocationID,
        DOlocationID,
        TIMESTAMP_DIFF(dropOff_datetime, pickup_datetime, SECOND) AS trip_duration,
        EXTRACT(YEAR FROM pickup_datetime) AS year,
        EXTRACT(MONTH FROM pickup_datetime) AS month
    FROM `zoompcamp2025.dbt_mliu.dim_fhv_trips`
),
p90_travel_time AS (
    SELECT 
        PUlocationID,
        DOlocationID,
        year,
        month,
        PERCENTILE_CONT(trip_duration, 0.90) OVER (
            PARTITION BY year, month, PUlocationID, DOlocationID
        ) AS p90
    FROM trip_duration
    GROUP BY PUlocationID, DOlocationID, year, month
)
SELECT 
    z.zone AS dropoff_zone,  
    p.p90
FROM p90_travel_time p
JOIN `zoompcamp2025.dbt_mliu.dim_zones` z 
    ON p.DOlocationID = z.locationid
JOIN `zoompcamp2025.dbt_mliu.dim_zones` pu_z
    ON p.PUlocationID = pu_z.locationid
    AND pu_z.zone IN ('Newark Airport', 'SoHo', 'Yorkville East')
WHERE 
    p.year = 2019 
    AND p.month = 11
ORDER BY p.p90 DESC
LIMIT 2 OFFSET 1;  -- Fetch the 2nd longest P90 travel time
