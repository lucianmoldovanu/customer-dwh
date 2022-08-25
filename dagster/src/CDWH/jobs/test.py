from dagster import job
from dagster_dbt import dbt_cli_resource

import CDWH.ops.main as ops

my_dbt_cli_resource = dbt_cli_resource.configured({
    "project_dir": "DBT"
})

@job(resource_defs={'dbt': my_dbt_cli_resource})
def test_dbt():
    ops.run_dbt_test()