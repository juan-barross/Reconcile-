-- Como o marketing responde, do jeito que a área faria sozinha.
--
-- Lojistas conquistados: todo lead que virou contrato, no mês do PRIMEIRO
-- CONTATO. É o mês em que a campanha trouxe o lead, então é o mês que o
-- marketing quer ver creditado.
--
-- Clientes novos: compradores no mês, contados por customer_id, que é a
-- coluna que o CRM exporta. A Olist gera um customer_id novo a cada pedido.

select
    'marketing' as area,
    'lojistas conquistados' as pergunta,
    strftime(m.first_contact_date, '%Y-%m') as mes,
    count(*) as valor
from staging.stg_olist__closed_deals as d
inner join staging.stg_olist__marketing_qualified_leads as m
    on d.mql_id = m.mql_id
group by 3

union all

select
    'marketing' as area,
    'clientes novos' as pergunta,
    strftime(o.purchased_at, '%Y-%m') as mes,
    count(distinct o.customer_id) as valor
from staging.stg_olist__orders as o
group by 3
