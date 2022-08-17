with raw_catalogs as (
    select * from {{ source('commercial', 'catalogs') }}
)

select * from raw_catalogs