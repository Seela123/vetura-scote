{{ config(materialized='table') }}

select *
from {{ source('local_files', 'cars_table') }}
