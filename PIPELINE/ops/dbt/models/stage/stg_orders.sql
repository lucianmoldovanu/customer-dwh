{{ config(materialized='view') }}

with logs as (
    select * from {{ ref('stg_weblogs') }}
),

orders as (
    select * from {{ source('commercial', 'orders') }}
),

orders_all_past_logins as (
    select
        ord.id as order_id,
        first_value(logs.country_code) over (partition by ord.ID order by logs.ts desc) as last_login_country_code,
        first_value(logs.ts) over (partition by ord.ID order by logs.ts desc) as last_login_ts
    from orders ord
    left join logs logs on ord.customer = logs.user_a and logs.ts <= ord.transaction_timestamp
),

orders_last_past_login as (
    select
        order_id,
        min(last_login_country_code) as last_login_country_code,
        min(last_login_ts) as last_login_ts
    from orders_all_past_logins
    group by order_id
),

final as (
    select
        ord.*,
        olog.last_login_country_code,
        olog.last_login_ts
    from orders ord
    left join orders_last_past_login olog on ord.id = olog.order_id
)

select * from final