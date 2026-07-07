with orders as (

    select * from {{ ref('stg_orders') }}

),

payments as (

    select
        order_id,
        sum(amount) as order_total,
        count(*) as payment_count
    from {{ ref('stg_payments') }}
    group by order_id

)

select
    orders.order_id,
    orders.customer_id,
    orders.order_date,
    orders.status,
    coalesce(payments.order_total, 0) as order_total,
    coalesce(payments.payment_count, 0) as payment_count
from orders
left join payments
    on orders.order_id = payments.order_id
