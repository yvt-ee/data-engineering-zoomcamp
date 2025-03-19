{{
    config(
        materialized='view'
    )
}}

with licensesdata as (
  select *,
    row_number() over(partition by license_number, license_issue_date) as rn
  from {{ source('staging', 'pet_licensesdata') }}
  where license_number is not null 
)

select
    -- Convert update_time to Pacific Time (PST)
    DATETIME(TIMESTAMP(update_time), "America/Los_Angeles") AS update_time_pst,
    
    -- Ensure license_issue_date is a DATE
    SAFE_CAST(license_issue_date AS DATE) AS license_issue_date,

    -- Extract year, month, and day from the date
    EXTRACT(YEAR FROM SAFE_CAST(license_issue_date AS DATE)) AS year,
    EXTRACT(MONTH FROM SAFE_CAST(license_issue_date AS DATE)) AS month,
    EXTRACT(DAY FROM SAFE_CAST(license_issue_date AS DATE)) AS day,

    -- Ensure license_number is uppercase
    upper(license_number) as license_number,

    animal_s_name,
    species,
    primary_breed,
    secondary_breed,
    zip_code
from licensesdata
where rn = 1
