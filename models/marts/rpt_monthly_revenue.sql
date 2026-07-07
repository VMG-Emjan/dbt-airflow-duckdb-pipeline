with orders as (

    select * from {{ ref('fct_orders') }}
    where status in ('completed', 'shipped')

)

select
    date_trunc('month', order_date) as revenue_month,
    count(*) as order_count,
    round(sum(order_total), 2) as total_revenue,
    round(avg(order_total), 2) as avg_order_value
from orders
group by 1
order by 1
