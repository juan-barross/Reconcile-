-- Como o financeiro responde.
--
-- Receita: soma de tudo que foi pago (com juros de parcelamento e vouchers),
-- no mês da APROVAÇÃO do pagamento. Pedido sem data de aprovação não entra:
-- para o financeiro, dinheiro não aprovado não é receita. O status do pedido
-- não é olhado, então pagamento aprovado de pedido cancelado entra.

select
    'financeiro' as area,
    'receita' as pergunta,
    strftime(o.approved_at, '%Y-%m') as mes,
    sum(p.payment_value) as valor
from staging.stg_olist__order_payments as p
inner join staging.stg_olist__orders as o
    on p.order_id = o.order_id
where o.approved_at is not null
group by 3
