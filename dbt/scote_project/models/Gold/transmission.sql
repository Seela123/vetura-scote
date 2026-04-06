{{ config(
    schema='gold',
    materialized='table'
) }}


SELECT

  transmission,

  COUNT(transmission) AS total,

  ROUND(COUNT(transmission) * 100 / SUM(COUNT(transmission)) OVER(),2) AS percentage

FROM {{ref('silver')}}

GROUP BY transmission