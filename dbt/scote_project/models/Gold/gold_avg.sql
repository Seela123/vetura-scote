{{ config(
    schema='gold',
    materialized='table'
) }}

SELECT

    ROUND(AVG(price),0) AS avg_price,

    ROUND(AVG(km),0) AS avg_km,

    ROUND(AVG(year),0) AS avg_year

FROM {{ref('silver')}}