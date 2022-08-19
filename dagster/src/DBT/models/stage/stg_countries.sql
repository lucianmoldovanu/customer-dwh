{{ config(materialized='view') }}

with countries as (
    select
        country_code,
        min(country) as country
    from {{ source('web_logs', 'ip_country_cache') }}
    group by country_code
)

select * from countries