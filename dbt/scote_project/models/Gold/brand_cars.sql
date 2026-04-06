{{ config(
    schema='gold',
    materialized='table'
) }}


SELECT (brand || ' ' || brand_car) AS cars,

        COUNT(brand_car) AS total

    FROM public_silver.silver

    GROUP BY brand,brand_car

    ORDER BY total desc

        LIMIT 20