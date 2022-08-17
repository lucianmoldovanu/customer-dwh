with raw_products as (
    select * from {{ source('commercial', 'products') }}
)

select * from raw_products