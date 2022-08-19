with logs as (
    select * from {{ ref('stg_weblogs') }}
),

top_agents as (
    select
        USER_AGENT,
        COUNT(DISTINCT USER_A) AS USER_CNT
    from logs
    -- where datediff('DAYS', "TS", current_date) <= 90
    group by USER_AGENT
)

select * from top_agents