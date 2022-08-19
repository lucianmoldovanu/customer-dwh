with logs as (
    select * from {{ ref('stg_weblogs') }}
),

country_masterdata as (
    select * from {{ ref('stg_countries') }}
),

product_masterdata as (
    select * from {{ ref('stg_products') }}
),

user_country_recent_logins as (
    select
        user_a as user,
        country_code
    from logs
    -- where datediff('DAYS', ts, current_date) <= 90
    group by 1, 2
),

country_ranking_by_most_distinct_users as (
    select
        country_code,
        user_cnt,
        row_number() over (order by user_cnt desc) as country_rnk
    from (
        select
            country_code,
            count(*) as user_cnt
        from user_country_recent_logins
        group by country_code
    )
),

recent_top_products_by_country_product as (
    select
        product as product_id,
        last_login_country_code as customer_country_code,
        sum(qty) as qty
    from {{ ref('stg_orders') }}
    -- where datediff('DAYS', transaction_timestamp, current_date) <= 90
    group by 1, 2
),

top_country_stats as (
    select
        rnk.country_code,
        prd.product_id,
        sum(qty) as total_order_quantity
    from country_ranking_by_most_distinct_users rnk
    left join recent_top_products_by_country_product prd on rnk.country_code = prd.customer_country_code
    where rnk.country_rnk = 1 -- only top 1 country by distinct login users
    group by 1, 2
),

final as (
    select
        topc.country_code,
        co.country,
        topc.product_id,
        pr.name as product,
        topc.total_order_quantity
    from top_country_stats topc
    left join country_masterdata co on topc.country_code = co.country_code
    left join product_masterdata pr on topc.product_id = pr.id
)

select * from final