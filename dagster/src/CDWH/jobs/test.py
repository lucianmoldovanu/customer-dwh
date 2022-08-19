from dagster import job
from dagster_dbt import dbt_cli_resource
from dagster_snowflake import snowflake_resource

import CDWH.ops.main as ops

@job(resource_defs={'snowflake': snowflake_resource, 'dbt': dbt_cli_resource})
def test_dbt():
    ops.run_dbt_test()