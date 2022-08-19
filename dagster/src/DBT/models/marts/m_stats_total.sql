with stats as (
    select * from {{ ref('m_stats_by_vendor') }}
),

final as (
    select
        year,
        month,
        sum(num_orders) as num_orders,
        sum(total_amount) as total_amount
    from stats
    group by 1,2

)

select * from final