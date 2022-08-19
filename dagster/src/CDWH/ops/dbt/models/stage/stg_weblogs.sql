{%- set columns = adapter.get_columns_in_relation(ref('raw_weblogs')) -%}

with source_data as (
    select * from {{ ref('raw_weblogs') }}
),

ip_country_cache as (
    select * from {{ source('web_logs', 'ip_country_cache') }}
),

valid_data as (
    select
        {{ get_columns_except_prefix('raw_weblogs', 'CHECK_', 'dat') -}},
        cache.country_code
    from source_data dat
    left join ip_country_cache cache on dat.ip = cache.IP
    where "CHECK_TIMESTAMP_FORMAT" = true and "CHECK_LAST_FIELD_POPULATED" = true
)

select * from valid_data