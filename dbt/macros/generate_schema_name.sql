{#- Usa o nome do esquema como está (staging, intermediate, marts),
    sem o prefixo do target que o dbt põe por padrão. -#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}{{ target.schema }}{%- else -%}{{ custom_schema_name | trim }}{%- endif -%}
{%- endmacro %}
