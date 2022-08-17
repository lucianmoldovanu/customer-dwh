with stg_orders as (
    select * from {{ ref('stg_orders') }}
),

catalogs as (
    select * from {{ ref('stg_catalogs') }}
),

orders_with_supplier_prices as (
    select
        ord.*,
        ord.qty * cat.supplier_price as supplier_total_amount --the purchase price from the supplier multiplied by the order qty; total cost per order at which the vendor bought the sold products from the supplier
    from stg_orders ord
    left join catalogs cat on ord.product = cat.product
        and ord.vendor_company = cat.vendor_company
),

agg_sales_proceeds as (
    select
        year(transaction_timestamp) as year,
        month(transaction_timestamp) as month,
        vendor_company,
        product,
        count(*) as num_orders,
        sum(total_amount) as total_amount,
        sum(supplier_total_amount) as supplier_total_amount
    from orders_with_supplier_prices
    group by 1, 2, 3, 4
)

select * from agg_sales_proceeds