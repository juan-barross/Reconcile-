with fonte as (
    select * from {{ source('olist', 'marketing_qualified_leads') }}
)

select
    mql_id,
    cast(first_contact_date as date) as first_contact_date,
    landing_page_id,
    origin
from fonte
