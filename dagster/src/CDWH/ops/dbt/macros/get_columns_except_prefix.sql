{%- macro get_columns_except_prefix(in_target_table, in_except_col_prefix, in_table_prefix = "") %}
    {%- set columns = adapter.get_columns_in_relation(ref(in_target_table)) -%}

    {%- for col in columns if in_except_col_prefix not in col.name %}
        {{ "" if in_table_prefix == "" else in_table_prefix + "." }}{{ col.name }}
        {{- ',' if not loop.last -}}
    {% endfor -%}
{% endmacro %}