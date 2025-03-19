{{
    config(
        materialized='view'
    )
}}

with licensesdata as 
(
  select *,
    row_number() over(partition by license_number, license_issue_date) as rn
  from {{ source('staging', 'pet_licensesdata') }}
  where license_number is not null 
)


select
    DATETIME(TIMESTAMP(update_time), "America/Los_Angeles") AS update_time_pst,
    DATETIME(TIMESTAMP(license_issue_date), "America/Los_Angeles") AS license_issue_date_pst,
    upper(license_number) as license_number,
    animal_s_name,
    species,
    primary_breed,
    secondary_breed,
    zip_code
from licensesdata
where rn = 1
