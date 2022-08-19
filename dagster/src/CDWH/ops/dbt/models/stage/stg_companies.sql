with raw_companies as (
    select * from {{ source('commercial', 'companies') }}
)

select * from raw_companies