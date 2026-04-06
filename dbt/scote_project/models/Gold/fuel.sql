{{ config(
    schema='gold',
    materialized='table'
) }}

SELECT fuel,COUNT(fuel) AS total

FROM {{ref('silver')}}

GROUP BY fuel