with customers as (

    select * from {{ ref('stg_customers') }}

),

customer_orders as (

    select
        customer_id,
        count(*) as order_count,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        sum(order_total) as lifetime_value
    from {{ ref('fct_orders') }}
    where status != 'cancelled'
    group by customer_id

)

select
    customers.customer_id,
    customers.full_name,
    customers.country,
    customers.signup_date,
    coalesce(customer_orders.order_count, 0) as order_count,
    customer_orders.first_order_date,
    customer_orders.last_order_date,
    coalesce(customer_orders.lifetime_value, 0) as lifetime_value
from customers
left join customer_orders
    on customers.customer_id = customer_orders.customer_id
