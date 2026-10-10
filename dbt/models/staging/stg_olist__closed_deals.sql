with fonte as (
    select * from {{ source('olist', 'closed_deals') }}
)

select
    mql_id,
    seller_id,
    sdr_id,
    sr_id,
    cast(won_date as timestamp) as won_at,
    business_segment,
    lead_type,
    lead_behaviour_profile,
    cast(has_company as boolean) as has_company,
    cast(has_gtin as boolean) as has_gtin,
    average_stock,
    business_type,
    cast(declared_product_catalog_size as double) as declared_product_catalog_size,
    cast(declared_monthly_revenue as decimal(14, 2)) as declared_monthly_revenue
from fonte
