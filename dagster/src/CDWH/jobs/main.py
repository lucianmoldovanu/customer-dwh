import os

from dagster import job
from dagster_snowflake import snowflake_resource
from dagster_dbt import dbt_cli_resource

import CDWH.ops.main as ops
from CDWH.ops.refresh_mock_data import refresh_mock
from CDWH.ops.weblogs_generate_mock_file import generate_weblog_file
from CDWH.ops.weblogs_transfer import transfer_weblogs

# arguments
SNOWFLAKE_DB = 'CDWH'
SNOWFLAKE_SCHEMA = 'CORE'
SNOWFLAKE_WAREHOUSE = 'CDWH_WH'

my_snowflake_resource = snowflake_resource.configured({
    "account": os.environ['SNOWFLAKE_HOST'],
    "user": os.environ['SNOWFLAKE_USER'],
    "password": os.environ['SNOWFLAKE_PASS'],
    "database": SNOWFLAKE_DB,
    "schema": SNOWFLAKE_SCHEMA,
    "warehouse": SNOWFLAKE_WAREHOUSE
})

my_dbt_cli_resource = dbt_cli_resource.configured({
    "project_dir": "DBT"
})

@job(resource_defs={'snowflake': my_snowflake_resource, 'dbt': my_dbt_cli_resource})
def build_datamodel_populate_mock():
    a = ops.refresh_b2b_data_model()
    mockdata = refresh_mock(a)

    ws_setup = ops.weblogs_setup(a)
    ws_gen = generate_weblog_file(mockdata)
    ws_trans = transfer_weblogs(ws_gen, ws_setup)
    ws_load = ops.weblogs_load(ws_trans)

    ops.run_dbt_all(ws_load)

# testing
if __name__ == "__main__":
    build_datamodel_populate_mock()