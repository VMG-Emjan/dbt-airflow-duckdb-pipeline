-- An order total below zero means a payment was recorded incorrectly.
select
    order_id,
    order_total
from {{ ref('fct_orders') }}
where order_total < 0
