-- as web logs are imported in raw form into DWH and processed by DBT, there is the risk that some rows may not be processable by regex
select * from {{ ref('raw_weblogs') }}
where not("CHECK_TIMESTAMP_FORMAT" = true and "CHECK_LAST_FIELD_POPULATED" = true)