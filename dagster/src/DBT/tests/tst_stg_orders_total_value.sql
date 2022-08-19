with raw_orders as (
    select * from {{ source('commercial', 'orders') }}
),

stg_orders as (
    select * from {{ ref('stg_orders') }}
)

select
    coalesce(r.id, '') || coalesce(s.id, '') as order_id_raw_stage
from raw_orders r
full outer join stg_orders s on r.id = s.id
where r.qty is null 
    or s.qty is null
    or r.total_amount is null
    or s.total_amount is null
    or abs(r.total_amount - s.total_amount) >= 0.001