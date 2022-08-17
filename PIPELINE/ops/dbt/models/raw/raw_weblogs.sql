{%- set rgx = '([0-9\.]*) ([a-zA-Z0-9-]*) ([a-zA-Z0-9]*) ([0-9-]* [0-9:\.]*) ([GET|POST]+) ([a-zA-Z/]*) (HTTP/[0-9\.]+) ([2|4|5][0-9]{2}) ([0-9]*) ([a-zA-Z/-]*) (.*)' -%}

{%- set fields = ['ip', 'USER_I', 'user_a', 'TS', 'METHOD', 'PATH', 'PROTO', 'RESP_CODE', 'PAYLOAD_SIZE', 'REFERRER', 'USER_AGENT'] -%}

with source_data as (
    select * from {{ source('web_logs', 'wlogs') }}
),

raw_data as (
    select
        {%- for fld in fields %}
        REGEXP_SUBSTR("LOG", '{{rgx}}', 1, 1, 'c', {{loop.index0 + 1}}) AS {{fld}}
        {{- ',' if not loop.last -}}
        {% endfor %}
    from source_data
),

data_with_checks as (
    select
        *,
        case when try_cast("TS" as timestamp) is null then false else true end as "CHECK_TIMESTAMP_FORMAT",
        case when length("USER_AGENT") > 0 then true else false end as "CHECK_LAST_FIELD_POPULATED"
    from raw_data
)

select * from data_with_checks