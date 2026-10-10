-- Como o time comercial responde.
--
-- Lojistas conquistados: contratos assinados, no mês do FECHAMENTO. É a data
-- que entra na meta do vendedor.
--
-- Receita: preço dos itens + frete, no mês da COMPRA, de todo pedido que tem
-- item, inclusive cancelado e indisponível. É o valor "vendido" (GMV).

select
    'vendas' as area,
    'lojistas conquistados' as pergunta,
    strftime(won_at, '%Y-%m') as mes,
    count(*) as valor
from staging.stg_olist__closed_deals
group by 3

union all

select
    'vendas' as area,
    'receita' as pergunta,
    strftime(o.purchased_at, '%Y-%m') as mes,
    sum(i.price + i.freight_value) as valor
from staging.stg_olist__order_items as i
inner join staging.stg_olist__orders as o
    on i.order_id = o.order_id
group by 3
