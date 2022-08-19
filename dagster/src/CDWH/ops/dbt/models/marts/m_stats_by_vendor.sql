with sales as (
    select * from {{ ref('m_sales_proceeds') }}
),

companies as (
    select * from {{ ref('stg_companies') }}
),

agg_sales_with_profitability as (
    select
        year,
        month,
        vendor_company as vendor_company_ID,
        sum(num_orders) as num_orders,
        sum(total_amount) as total_amount,
        sum(supplier_total_amount) as supplier_total_amount,
        100 * (sum(total_amount) / sum(supplier_total_amount) - 1) as profit_rate_perc
    from sales sal
    group by 1, 2, 3
),

final as (
    select
        sal.*,
        co.name as vendor_company
    from agg_sales_with_profitability sal
    left join companies co on sal.vendor_company_ID = co.ID
)

select * from final