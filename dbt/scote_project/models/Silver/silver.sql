{{ config(
    schema='silver',
    materialized='table'
) }}


SELECT
    id,

    NULLIF(TRIM(name), ' ') AS name,

    NULLIF(price::numeric,0) as price,

    TRIM(brand) AS brand,

    TRIM(REPLACE(subbrand,'i','I')) AS brand_car,

    TRIM(REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(
                                fuel::text,
                                'Electric (plug-in) / petrol', 'electric benzin'),
                            'Diesel/Elektro', 'electric diesel'),
                        'Elektrischer Strom', 'electric power'),
                    'Benzin/Elektro-PlugIn', 'electric benzin'),
                'Benzin bleifrei', 'benzine'),
                'benzine', 'benzin'),
                'Benzin', 'benzin'),
            'Benzin/Elektro', 'electric benzin'),
        'Petrol', 'benzin'))
    AS fuel,

    km,

    TRIM(
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    COALESCE(NULLIF(transmission::text, ' '), 'Unknown'),
                    'Automatik', 'Automatic'
                ),
                'Manuelles', 'Manual'
            ),
            'Manual Getriebe', 'Manual'
        ),
        'Direktantrieb', 'Automatic'
    )
) AS transmission,

    TRIM(city) AS city,
    year

FROM {{ref('bronze_raw')}}
WHERE price > 1000
AND year >= 1900 AND year <= 2026