{{
    config(
        materialized='table'
    )
}}


select *
from {{ ref('stg_pet_licensesdata') }}