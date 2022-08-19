with orders as (
    select * from {{ ref('stg_orders') }}
),

country_masterdata as (
    select * from {{ ref('stg_countries') }}
),

product_masterdata as (
    select * from {{ ref('stg_products') }}
),

product_sales_by_country as (
    select
        last_login_country_code as country_code,
        product as product_ID,
        sum(qty) as total_sales_units
    from orders
    -- where datediff('DAYS', transaction_timestamp, current_date) <= 90
    group by 1,2
),

product_rank_by_country as (
    select
        country_code,
        product_ID,
        total_sales_units,
        row_number() over (partition by country_code order by total_sales_units desc, product_ID) as rank
    from product_sales_by_country
),

top_product_by_country as (
    select
        rnk.country_code,
        cnt.country,
        rnk.product_ID,
        prod.name as product,
        total_sales_units
    from product_rank_by_country rnk
    left join country_masterdata cnt on rnk.country_code = cnt.country_code
    left join product_masterdata prod on rnk.product_ID = prod.ID
    where rnk.rank = 1
)

select * from top_product_by_country